import pickle
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from backtesting.dash_app import entry_exit_analysis
from backtesting.dash_app import monthly_analysis
from backtesting.dash_app import trading_history
from backtesting.dash_app import dash_report

from backtesting.dash_app.app import app


def get_backtesting_report_dash_app(backtesting_result: dict):
    app.layout = html.Div([
        html.H2('Backtesting Result'),
        dcc.Location(id='url', refresh=False),
        dcc.Link('General Performance', href='/btPerformance'),
        html.Br(),
        dcc.Link('Monthly Analysis', href='/monthlyAnalysis'),
        html.Br(),
        dcc.Link('Entry and exit Detail', href='/details'),
        html.Br(),
        dcc.Link('Trading history', href='/history'),
        html.Br(),
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
            return monthly_analysis.layout
        elif pathname == '/details':
            return entry_exit_analysis.layout
        elif pathname == 'history':
            return trading_history.layout
        else:
            return index_page
    return app


if __name__ == '__main__':
    # app.run_server(host='127.0.0.1', debug=True)
    with open(r'../backtesting_result_sample.pickle', 'rb') as f:
        backtesting_result = pickle.load(f)
    _app = get_backtesting_report_dash_app(backtesting_result)
    _app.run_server(host='127.0.0.1', debug=True)
