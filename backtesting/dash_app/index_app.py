import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from backtesting.backtesting_metric import aggregate_returns
from backtesting.dash_app import entry_exit_analysis
from backtesting.dash_app import monthly_analysis
from backtesting.dash_app import trading_history
from backtesting.dash_app import dash_report

from backtesting.dash_app.app import app
from backtesting.plotting import aggregate_returns_heatmap, returns_distribution_plot

backtesting_result = None
def get_backtesting_report_dash_app(backtesting_result: dict):
    app.layout = html.Div([
        html.H2('Backtesting Result'),
        dcc.Location(id='url', refresh=False),
        dcc.Link('General Performance', href='/btPerformance'),
        # dcc.Tab(),
        html.Br(),
        dcc.Link('Monthly Analysis', href='/monthlyAnalysis'),
        html.Br(),
        dcc.Link('Entry and exit Detail', href='/details'),
        html.Br(),
        dcc.Link('Trading history', href='/history'),
        html.Br(),
        # dcc.Tabs(id='tabs', value='tab', children=[
        #     dcc.Tab(label='General Performance', value='tab-1'),
        #     dcc.Tab(label='Monthly Analysis', value='tab-2'),
        #     dcc.Tab(label='Entry and exit Detail', value='tab-3'),
        #     dcc.Tab(label='Trading history', value='tab-4'),
        #     # dcc.Tab(label='Tab two', value='tab-2'),
        # ]),

        html.Div(id='page-content'),
    ], style={'margin': '30px'})

    index_page = html.Div([
        # todo 行情profile
        # benchmark
        # each stock
        # each time frame
        # strategy basic information
        # name

        # todo 回测类型
        #
    ]),

    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/btPerformance':
            return dash_report.get_layout(backtesting_result)
        elif pathname == '/monthlyAnalysis':
            return monthly_analysis.get_layout(backtesting_result)
        elif pathname == '/details':
            return entry_exit_analysis.get_layout(backtesting_result)
        elif pathname == '/history':
            return trading_history.get_layout(backtesting_result)
        else:
            return index_page

    @app.callback([Output('title', 'children'),
                   Output('return-heatmap', 'figure'),
                   Output('returns-distribution', 'figure')
                   ], [Input('dropdown', 'value')])
    def change_selection(value):
        if value == 'D':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'day')
            heatmap = aggregate_returns_heatmap(agg_ret, 'day')
            displot = returns_distribution_plot(agg_ret)
            return 'Daily Analysis', heatmap, displot
        elif value == 'W':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'week')
            heatmap = aggregate_returns_heatmap(agg_ret, 'week')
            displot = returns_distribution_plot(agg_ret)
            return 'Weekly Analysis', heatmap, displot
        elif value == 'M':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'month')
            heatmap = aggregate_returns_heatmap(agg_ret, 'month')
            displot = returns_distribution_plot(agg_ret)
            return 'Monthly Analysis', heatmap, displot
        elif value == 'Q':

            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'quarter')
            heatmap = aggregate_returns_heatmap(agg_ret, 'quarter')
            displot = returns_distribution_plot(agg_ret)
            return 'Quarter Analysis', heatmap, displot

    @app.callback(
        Output('table', 'data'),
        [Input('date-picker-range', 'start_date'),Input('date-picker-range', 'end_date')])
    def update_output(date_from, date_to):
        if date_to is None or date_from is None:
            return
        df = backtesting_result['trade_list']
        df_ = df[(df['order_time']>=pd.to_datetime(date_from)) & (df['order_time']<=pd.to_datetime(date_to))]
        return df_.to_dict('records')

      
    return app


if __name__ == '__main__':
    # app.run_server(host='127.0.0.1', debug=True)
    with open(r'../backtesting_result_sample.pickle', 'rb') as f:
        backtesting_result = pickle.load(f)
    _app = get_backtesting_report_dash_app(backtesting_result)
    _app.run_server(host='127.0.0.1', debug=True,port=8005)
