import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

pio.renderers.default = "browser"


def orderbook_plot(orderbook):
    bid = np.array(orderbook['Bid'])
    ask = np.array(orderbook['Ask'])

    bid_x = bid[:, 1]
    bid_y = bid[:, 0] - bid[:, 0][0]
    ask_x = ask[:, 1]
    ask_y = ask[:, 0] - ask[:, 0][0]
    bid_vwap = np.sum(bid[:, 1] * bid[:, 0]) / np.sum(bid[:, 1]) - bid[:, 0][0]
    ask_vwap = np.sum(ask[:, 1] * ask[:, 0]) / np.sum(ask[:, 1]) - ask[:, 0][0]

    bid_bar = go.Bar(
        x=bid_x,
        y=bid_y, width=bid_x / 5,
        orientation='h', name='Bid', marker=dict(
            color='red', ), )
    ask_bar = go.Bar(
        x=ask_x,
        y=ask_y, width=ask_x / 5,
        orientation='h', name='Ask', marker=dict(
            color='green', ))

    fig = go.Figure(data=[bid_bar, ask_bar])
    fig.add_shape(
        # Line Horizontal
        type="line",
        x0=0,
        y0=bid_vwap,
        x1=10,
        y1=bid_vwap,
        line=dict(
            color="#FF2D2D",
            width=4,
            dash="solid",
        ),
    )
    fig.add_shape(
        # Line Horizontal
        type="line",
        x0=0,
        y0=ask_vwap,
        x1=10,
        y1=ask_vwap,
        line=dict(
            color="#00EC00",
            width=4,
            dash="solid",
        ),
    )
    fig.update_layout(yaxis_tickformat='g')
    return fig


def tick_plot(tick_df, freq='1T'):
    def order_flow(x):
        if x['ticker_direction'] == 'BUY':
            return x['price'] * x['volume']
        elif x['ticker_direction'] == 'SELL':
            return - x['price'] * x['volume']
        elif x['ticker_direction'] == 'NEUTRAL':
            return 0

    tick_df['order_flow'] = tick_df.apply(order_flow, axis=1)
    agg = tick_df.groupby('time').agg({'order_flow': 'sum', 'price': 'last'})
    agg = agg.groupby(pd.Grouper(freq=freq)).agg({'order_flow': 'sum', 'price': 'last'})
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    vol_bar = go.Bar(x=agg.index, y=agg['order_flow'])
    price_line = go.Scatter(x=agg.index, y=agg['price'], mode='lines')
    fig.add_trace(vol_bar, secondary_y=True, )
    fig.add_trace(price_line, secondary_y=False, )
    # fig.update_layout(hoverdistance=0)
    # fig.update_traces(xaxis='x', hoverinfo='none')
    fig.update_xaxes(showspikes=True, spikemode='across', spikesnap='data', showline=True, spikedash='solid')
    fig.update_layout(yaxis_tickformat='g')


    fig.show()
    return fig

def bid_ask_plot():
    pass


def triple_screen_plot():
    pass


if __name__ == '__main__':
    sample = {'_id': {'$oid': '5f22eac623de44d2b46056ce'},
              'code': 'HK.999010',
              'svr_recv_time_bid': '2020-07-30 23:44:06.596',
              'svr_recv_time_ask': '2020-07-30 23:44:06.596',
              'Bid': [[24476.0, 1, 1],
                      [24475.0, 4, 3],
                      [24474.0, 2, 2],
                      [24473.0, 4, 4],
                      [24472.0, 3, 3],
                      [24471.0, 2, 2],
                      [24470.0, 8, 3],
                      [24469.0, 3, 3],
                      [24468.0, 2, 2],
                      [24467.0, 3, 3]],
              'Ask': [[24477.0, 1, 1],
                      [24478.0, 2, 2],
                      [24479.0, 4, 4],
                      [24480.0, 2, 2],
                      [24481.0, 4, 4],
                      [24482.0, 3, 3],
                      [24483.0, 5, 5],
                      [24484.0, 4, 4],
                      [24485.0, 7, 5],
                      [24486.0, 3, 3]]}
    # orderbook_plot(sample).show()
    rt_df = pd.read_csv('2020-07-30.csv')
    rt_df = rt_df[rt_df['code'] == 'HK.999010']
    rt_df['time'] = pd.to_datetime(rt_df['time'])
    rt_df['hours'] = rt_df['time'].apply(lambda x: x.hour)

    rt_df = rt_df[(rt_df['hours'] >= 9) & (rt_df['hours'] <= 12)]
    tick_plot(rt_df)
