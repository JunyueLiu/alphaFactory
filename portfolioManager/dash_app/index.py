from datetime import timedelta

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from portfolioManager.dash_app.app import app
from portfolioManager.plotting import net_values_plot, corr_heatmap, holding_line_plot, efficient_frontier_plot
from portfolioManager.utils import *
from portfolioManager.dash_app import strategy_allocation


def get_pm_report_dash_app(portfolio: dict = None):
    # portfolio
    # {
    #   'strategy_1':{
    #   'net_value': pd.Series,
    #   'position': pd.Series
    #
    #
    #
    #   }
    # }
    net_values = to_net_value_df(portfolio)
    pos = to_position_df(portfolio)
    instruments = pos.index.get_level_values(1).unique().to_list()

    min_date = net_values.index.get_level_values(0).min().date()
    max_date = net_values.index.get_level_values(0).max().date()

    net_values_ts_plot = net_values_plot(net_values)
    rets = net_values.pct_change()
    corr_heatmap_plot = corr_heatmap(rets.corr())

    app.layout = html.Div([
        html.H1('Strategy Comparison'),
        html.Div([
            dcc.Location(id='url', refresh=False),
            dcc.Link('Index', href='/'),
            html.Br(),
            dcc.Link('Portfolio Allocation', href='/allocation'),
            html.Div(id='page-content')
        ],
        ),

    ])
    index_page = html.Div([
        dcc.Graph(figure=net_values_ts_plot),
        dcc.Graph(figure=corr_heatmap_plot),
        dcc.Dropdown(id='asset-selection',
                     options=[
                         {'label': i, 'value': i} for i in instruments

                     ], value=instruments[0]),
        dcc.DatePickerRange(id='date-range',
                            min_date_allowed=min_date,
                            max_date_allowed=max_date,
                            initial_visible_month=max_date,
                            start_date=max_date - timedelta(days=20),
                            end_date=max_date
                            ),
        dcc.Graph(id='holding'),
        # dcc.Dropdown(id='date-selection',
        #              options=[
        #                  {'label': i, 'value': i} for i in pos.index.get_level_values(0).unique().to_list()
        #              ]),
        dcc.Graph(id='holding-pie'),

    ])

    # ------------------ index page ------------------
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/':
            return index_page
        elif pathname == '/allocation':
            return strategy_allocation.get_layout(net_values)

    @app.callback([Output('holding', 'figure')],
                  [Input('asset-selection', 'value'),
                   Input('date-range', 'start_date'),
                   Input('date-range', 'end_date'), ])
    def update_holding(instrument, start_date, end_date):
        return holding_line_plot(pos, instrument, start_date, end_date),

    # ------------------ allocation page ------------------

    @app.callback([Output('efficient-frontier', 'figure'),
                   ],
                  [Input('update', 'n_clicks')],
                  [State('hidden-ret', 'children'),
                   State('hidden-cov', 'children'),
                   State('weights', 'children'),
                   State('hidden-weights', 'children'),
                   State('annualized-factor', 'value'),
                   State('efficient-frontier', 'figure')],
                  )
    def update_efficient_frontier(n_clicks, ret, cov, weights, hidden_weights, factor, ef):
        ret = pd.read_json(ret)
        cov_matrix = pd.read_json(cov)

        annualized_ret_mean = int(factor) * ret.mean()
        annualized_ret_cov = int(factor) * cov_matrix.cov()
        annualized_ret_std = np.sqrt(factor) * ret.std()

        weights_dict = {}
        for w in weights:
            if w['type'] == 'Input':
                id = w['props']['id']
                value = float(w['props']['value']) / 100
                weights_dict[id] = value

        allocation = pd.DataFrame([weights_dict])
        allocation = allocation.T
        allocation.columns = ['allocation']
        hidden_allocation = pd.read_json(hidden_weights).apply(lambda x: round(x, 4))
        if ef is None or allocation.to_dict() != hidden_allocation.to_dict():
            ef = efficient_frontier_plot(annualized_ret_mean, annualized_ret_cov, annualized_ret_std, allocation)
        return ef,

    @app.callback([Output('portfolio-netvalue', 'figure')],
                  [Input('update', 'n_clicks')],
                  [State('weights', 'children'),
                   State('hidden-netvalue', 'children')])
    def update_net_value(n_clicks, weights, net_value):

        weights_dict = {}
        net_value = pd.read_json(net_value)
        for w in weights:
            if w['type'] == 'Input':
                id = w['props']['id']
                value = float(w['props']['value']) / 100
                weights_dict[id] = value
        net_value_ = net_value.copy()
        for col in net_value.columns:
            net_value_[col] = net_value_[col] * weights_dict[col]
        net_value['portfolio'] = net_value_.sum(axis=1)
        net_value['portfolio'] = net_value['portfolio'] / net_value['portfolio'][0]
        nv_plot = net_values_plot(net_value)
        return nv_plot,

    return app


if __name__ == '__main__':
    portfolio = load_result_from_pickles(r'../sample_data')
    portfolio = normalized_net_value(portfolio)
    # print(portfolio)
    app_ = get_pm_report_dash_app(portfolio)
    app.run_server(host='127.0.0.1', port=8065)
