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

    @app.callback([Output('efficient-frontier', 'figure')],
                  [Input('hidden-ret', 'children'),
                   Input('hidden-cov', 'children'),
                   Input('hidden-weights', 'children'),
                   Input('annualized-factor', 'value')])
    def update_weights(ret, cov, weights, factor):
        ret = pd.read_json(ret)
        cov_matrix = pd.read_json(cov)
        # allocation = pd.read_json(weights)
        annualized_ret_mean = int(factor) * ret.mean()
        annualized_ret_cov = int(factor) * cov_matrix.cov()
        annualized_ret_std = np.sqrt(factor) * ret.std()
        allocations1 = calculate_max_sharp_weights(annualized_ret_mean, annualized_ret_cov)
        a1_ret, a1_std = calculate_portfolio_ret_std(allocations1.values.reshape(-1), annualized_ret_mean, annualized_ret_cov)
        allocations2 = calculate_min_variance_weights(annualized_ret_mean, annualized_ret_cov)
        a2_ret, a2_std = calculate_portfolio_ret_std(allocations2.values.reshape(-1), annualized_ret_mean, annualized_ret_cov)

        # allocations_dict = allocations.to_dict()
        # print(weights_children)
        returns_range = np.linspace(annualized_ret_mean.min(), annualized_ret_mean.max(), 100)
        frontier = efficient_frontier(annualized_ret_mean, annualized_ret_cov, returns_range)
        ef = efficient_frontier_plot(annualized_ret_mean, annualized_ret_std,
                                     a1_ret, a1_std,
                                     a2_ret, a2_std,
                                     returns_range, frontier)

        return ef,
        pass
    return app

if __name__ == '__main__':
    portfolio = load_result_from_pickles(r'../sample_data')
    portfolio = normalized_net_value(portfolio)
    # print(portfolio)
    app_ = get_pm_report_dash_app(portfolio)
    app.run_server(host='127.0.0.1', debug=True)
