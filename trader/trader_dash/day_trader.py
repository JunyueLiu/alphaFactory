import json
import pickle
import dash_table
import inspect
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from gateway.futu_quote import *
from gateway.futu_brokerage import *

from trader.trader_dash.app import app as app_


def get_daytrader_dash_app(futu_quote, futu_brokerage, dash_app=None):
    # global app
    if dash_app is not None:
        app = dash_app
    else:
        app = app_
    app.layout = html.Div([
        html.H2('DayTrader'),
        dcc.Location(id='url', refresh=False),
        dcc.Link('Index', href='/'),
        html.Br(),
        dcc.Link('CBBC Trader', href='/cbbc_trader'),
        # dcc.Tab(),
        html.Br(),
        dcc.Link('Futures', href='/futures'),
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






    return app


if __name__ == '__main__':
    quote = FutuQuote()
    brokerage = FutuBrokerage()
    get_daytrader_dash_app(quote, brokerage).run_server(host='localhost', debug=True)
