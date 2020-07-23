import json
import pickle
import dash_table
import inspect
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from plotly import graph_objects as go

import dash
import futu

from dash.dependencies import Input, Output, State
import pandas as pd

from gateway.brokerage_base import BrokerageBase
from gateway.quote_base import QuoteBase
from graph.bar_component import candlestick
from graph.indicator_component import volume
from graph.stock_graph import stick_and_volume


from trader.trader_dash.demoQuote import DemoQuote


def get_live_dash_app(quote: QuoteBase, brokerage: BrokerageBase = None, holding=None, app=None,
                      init_subscribe: dict = None):
    if app is None:
        external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div([
        html.Div([
            html.Div([
                html.H2(id='trade-time'),
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
                html.Div([dcc.Dropdown(id='code'),
                          dcc.Dropdown(id='graph-sub')]
                         ),

                dcc.Graph(id='main-chart')]

            ),

        ], style={'float': 'left', 'width': '60%'},

        ),

        html.Div([

            html.Div([
                html.Div([dcc.Input(id='unlock-token', placeholder='password to unlock'),
                          html.Button(children='unlock', id='unlock-button')]),
                html.Div('Strategy Group'),
                dcc.Dropdown(id='strategy-selection'),

                dash_table.DataTable(
                    id='holding',
                    columns=[{"name": i, "id": i} for i in ['Code', 'Amount', 'Cost', 'Equity', 'PnL', 'Percentage']],
                )

            ], style={'overflow': 'auto', 'height': '200px'}),

            html.Div(
                dash_table.DataTable(
                    id='sub-live',
                    columns=[{"name": i, "id": i} for i in ['Code', 'Bid', 'Ask', 'Bid Amount', 'Ask Amount']],
                )
                , style={'overflow': 'auto', 'height': '180px'}
            ),

            html.Div([
                html.H5('Trade board'),
                dcc.Input(id='trade-code', placeholder='Trade code'),
                dcc.Input(id='trade-amount', type='number'),
                dcc.Dropdown(id='order-type',
                             options=[{'label': i, 'value': i}
                                      for i in [
                                          "NORMAL",  # 普通订单(港股的增强限价单、A股限价委托、美股的限价单)
                                          "MARKET",  # 市价，目前仅美股
                                          "ABSOLUTE_LIMIT",  # 港股_限价(只有价格完全匹配才成交)
                                          "AUCTION",  # 港股_竞价
                                          "AUCTION_LIMIT",  # 港股_竞价限价

                                      ]]
                             ),
                html.Button(id='submit-order', children='Submit'),
            ]
            ),
            html.Div([
                html.H5('Order list'),
                dash_table.DataTable(
                    id='order-live',
                    columns=[{"name": i, "id": i} for i in ['Code', 'Amount', 'Direction', 'OrderType', 'Status']],
                )]
                , style={'overflow': 'auto', 'height': '180px'}

            ),

        ], style={'float': 'right', 'width': '35%'}
        ),

        dcc.Interval(
            id='interval-component-second',
            interval=5 * 1000,  # in milliseconds
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
            if init_subscribe is not None and subscribed is None:
                # subscribed = json.dumps(init_subscribe)
                subscribed = {}
                for c, sub_list in init_subscribe.items():
                    ret = quote.subscribe([c], sub_list)
                    if ret[0] == 0:
                        if c in subscribed:
                            subscribed[c].extend(sub_type)
                        else:
                            subscribed[c] = sub_type
                option = [{'label': i, 'value': i} for i in subscribed.keys()]
                return 'success:'.format(init_subscribe), json.dumps(init_subscribe), option

        else:
            return None, json.dumps({}), []

        subscribed = json.loads(subscribed)
        ret = quote.subscribe([code], sub_type)
        if ret[0] == 0:
            if code in subscribed:
                subscribed[code].extend(sub_type)
            else:
                subscribed[code] = sub_type
        # print(subscribed)
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

    @app.callback(Output('main-chart', 'figure'),
                  [Input('interval-component-second', 'n_intervals'),
                   ],
                  [State('code', 'value'), State('graph-sub', 'value'),
                   ]
                  )
    def update_graph(n, code, sub):
        if code is None or sub is None:
            return go.Figure()
        # print(sub, code)
        ret, data = quote.get_cur_kline(code, 100, sub)
        # print(data)
        bar = candlestick(data, symbol=code)
        volume_c = volume(data, )
        fig = stick_and_volume(bar, volume_c,)
        layout = dict(plot_bgcolor='#fff', width=700, height=500,showlegend=False, xaxis_rangeslider_visible=False,)
        layout['xaxis1'] = dict(
                showline=False, showgrid=False
            )
        layout['yaxis1'] = dict(
            showline=False, showgrid=False
        )
        layout['xaxis2'] = dict(
            showline=False, showgrid=False
        )
        layout['yaxis2'] = dict(
            showline=False, showgrid=False
        )


        fig.update_layout(layout
                          )
        return fig

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
    sub = {
        '0700.HK': ["K_1M"],
        '1810.HK': ["K_1M"],
        '3690.HK': ["K_1M"],
        '9988.HK': ["K_1M"],

    }
    quote = DemoQuote()
    app_ = get_live_dash_app(quote, init_subscribe=sub)
    app_.run_server(host='localhost', port=8050, debug=True)
