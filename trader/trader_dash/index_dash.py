import json
import pickle
import dash_table
import inspect
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

import dash
import futu

from dash.dependencies import Input, Output, State
import pandas as pd

from gateway.brokerage_base import BrokerageBase
from gateway.quote_base import QuoteBase

from technical_analysis import momentum
from technical_analysis import pattern
from technical_analysis import volume
from technical_analysis import volatility
from technical_analysis import overlap
from technical_analysis import customization

from technical_analysis.momentum import *
from technical_analysis.pattern import *
from technical_analysis.volume import *
from technical_analysis.volatility import *
from technical_analysis.overlap import *
from technical_analysis.customization import *
from technical_analysis.utils import *
from trader.trader_dash.demoQuote import DemoQuote


def get_live_dash_app(quote: QuoteBase, brokerage: BrokerageBase = None, holding=None, app=None):

    if app is None:
        external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.Div([
            html.Div([
                dcc.Input(id='subscribe', placeholder='Input code to subscribe'),
                dcc.Dropdown(id='sub-type', options=[
                    {'label': i, 'value': i} for i in [
                        "K_1M", "K_3M", "K_5M", "K_15M",
                        "K_30M", "K_60M", "K_DAY", "K_WEEK",
                        "K_MON", "K_QUARTER", "K_YEAR"

                    ]

                ], multi=True, placeholder='Subscribe kline'),
                html.Button(children='subscribe', id='sub-submit', style={'display': 'inline-block',
                                                                          'margin-left': '5px', 'margin-top': '5px'})
                , html.Button(children='unsubscribe', id='unsub')],

            ),
            html.Div(id='sub-info'),
            html.Div([
                dcc.Dropdown(id='code'),
                dcc.Dropdown(id='graph-sub', ),
                dcc.Graph(id='main-chart', )]

            ),

        ], style={'float': 'left'},

        ),
        html.Div([
            html.Div([dcc.Input(id='unlock-token', placeholder='password to unlock'),
                      html.Button(children='unlock', id='unlock-button')])

        ], style={'float': 'right'}

        ),
        dcc.Interval(
            id='interval-component-second',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        ),
        # hidden
        html.Div(id='subscribed', style={'display': 'none'}),
    ])

    @app.callback([Output('sub-info', 'children'),
                   Output('subscribed', 'children'),
                   Output('code', 'options')],
                  [Input('sub-submit', 'n_clicks')],
                  [State('sub-type', 'value'),
                   State('subscribe', 'value'),
                   State('subscribed', 'children')])
    def subscribe(n_clicks, sub_type, code, subscribed):
        if code is None:
            return None, json.dumps({}), []
        print(subscribed)
        if subscribed is None:
            subscribed = {}
        else:
            subscribed = json.loads(subscribed)
        ret = quote.subscribe([code], sub_type)
        if ret[0] == 0:
            if code in subscribed:
                subscribed[code].extend(sub_type)
            else:
                subscribed[code] = sub_type
        print(subscribed)
        option = [{'label': i, 'value': i} for i in subscribed.keys()]

        return ret, json.dumps(subscribed), option

    @app.callback([Output('graph-sub', 'options')],
                  [Input('code', 'value')],
                  [State('subscribed', 'children')]
                  )
    def update_graph_sub(code, subscribed):
        if subscribed is None:
            return [],
        subscribed = json.loads(subscribed)
        if code is None:
            return [],
        options = [{'label': i, 'value': i} for i in subscribed[code]]
        return options,

    # @app.callback([Output('sub-info', 'children')],
    #               [Input('unsub', 'n_clicks')],
    #               [State('sub-type', 'value'),
    #                State('subscribe', 'value')])
    # def unsubscribe(n_clicks, sub_type, code):
    #     ret = quote.unsubscribe([code], sub_type)
    #     print(code, sub_type)
    #     return ret,

    return app


if __name__ == '__main__':
    quote = DemoQuote(None)
    app_ = get_live_dash_app(quote)
    app_.run_server(host='localhost', port=8050, debug=True)
