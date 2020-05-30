import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly
from dash.dependencies import Input, Output
from futu import *
import datetime
import dash_table

import pandas as pd
import numpy as np

from graph.bar_component import candlestick
from graph.indicator_component import no_overlap
import plotly.graph_objects as go

from technical_analysis.overlap import MA
from technical_analysis.momentum import MOM
from graph.stock_graph import stick_and_indicators

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(
    __name__,
    requests_pathname_prefix='/hsiIntraday/', external_stylesheets=external_stylesheets
)






hsi = 'HK.800000'

quote_ctx = OpenQuoteContext()
ret, msg = quote_ctx.subscribe([hsi], [SubType.K_1M])

last_day = None
now = datetime.datetime.now()
today = now.date()
ret, days = quote_ctx.get_trading_days(Market.HK)
if now.hour < 9 and today.strftime('%Y-%m-%d') == days[-1]['time']:
    tradeday = days[-2]['time']
else:
    tradeday = days[-1]['time']
morning_index = pd.period_range(start=tradeday + ' 9:30:00', end=tradeday + ' 12:00:00', freq='1T')
afternoon_index = pd.period_range(start=tradeday + ' 13:01:00', end=tradeday + ' 16:00:00', freq='1T')
index = morning_index.append(afternoon_index)
col_list = [
    'code', 'time_key', 'open', 'close', 'high', 'low', 'volume',
    'turnover', 'pe_ratio', 'turnover_rate', 'last_close'
]
intraday = pd.DataFrame(columns=col_list)
intraday['time_key'] = pd.to_datetime(index.to_timestamp())
intraday.set_index(['time_key'], inplace=True)
ret, history = quote_ctx.get_cur_kline(hsi, 400, ktype=SubType.K_1M)
print(history)
history['time_key'] = pd.to_datetime(history['time_key'])
history = history[history['time_key'] >= pd.to_datetime(tradeday)]
history.set_index(history['time_key'], inplace=True)
intraday.update(history)

class CurKlineTest(CurKlineHandlerBase):
    def on_recv_rsp(self, rsp_str):
        global intraday
        ret_code, data = super(CurKlineTest, self).on_recv_rsp(rsp_str)
        if ret_code != RET_OK:
            print("CurKlineTest: error, msg: %s" % data)
            return RET_ERROR, data

        # print("CurKlineTest ", data)  # CurKlineTest自己的处理逻辑
        timestamp = pd.to_datetime(data['time_key'][0])
        if timestamp.hour == 9 and timestamp.minute == 30:
            tradeday = timestamp.strftime('%Y-%m-%d')
            morning_index = pd.period_range(start=tradeday + ' 9:30:00', end=tradeday + ' 12:00:00', freq='1T')
            afternoon_index = pd.period_range(start=tradeday + ' 13:01:00', end=tradeday + ' 16:00:00', freq='1T')
            index = morning_index.append(afternoon_index)
            col_list = [
                'code', 'time_key', 'open', 'close', 'high', 'low', 'volume',
                'turnover', 'pe_ratio', 'turnover_rate', 'last_close'
            ]
            intraday = pd.DataFrame(columns=col_list)
            intraday['time_key'] = pd.to_datetime(index.to_timestamp())
            intraday.set_index(['time_key'], inplace=True)
        data['time_key'] = pd.to_datetime(data['time_key'])
        data.set_index(data['time_key'], inplace=True)
        intraday.update(data)
        return RET_OK, data

handler = CurKlineTest()
quote_ctx.set_handler(handler)

app.layout = html.Div(
    html.Div([
        html.H4(id='header_text'),
        # dcc.Input(id='')
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 500,  # in milliseconds
            n_intervals=0
        ),
        dcc.Interval(
            id='interval-component-second',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )
    ], style={'display': 'inline-block', 'width': '100%', 'height': '100%'})
)

# last_day = tradeday

@app.callback(Output('header_text', 'children'),
              [Input('interval-component-second', 'n_intervals')])
def update_tradeday(n):
    now = datetime.datetime.now()
    return 'HSI intraday {}'.format(now.strftime('%Y/%m/%d %H:%M:%S'))


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    kline = candlestick(intraday, None, symbol='HSI')
    intraday['ma5'] = MA(intraday, 5)
    intraday['ma10'] = MA(intraday, 10)
    intraday['ma20'] = MA(intraday, 20)
    intraday['mom'] = MOM(intraday, 10)
    # intraday['HT_TRENDLINE'] = HT_TRENDLINE('close')

    # intraday['mom_ma20'] = MOM(intraday, 1, price_type='ma20')

    # plotly.offline.plot(fig2, filename='file2.html')
    indicators = no_overlap(intraday, None, ['ma5', 'ma10', 'ma20', 'mom'])
    fig = stick_and_indicators(kline, indicators, [0, 0, 0, 1])

    # fig = stick_and_indicators(kline, indicators, [0, 0, 0, 1])
    fig.add_trace(
        go.Scatter(x=fig.data[0]['x'], y=intraday['last_close'][0] * np.ones(len(intraday)), name='last close')
    )

    fig.update_layout(
        autosize=False,
        # width=500,
        height=900,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ), yaxis_tickformat='g', xaxis_rangeslider_visible=False
    )

    return fig
