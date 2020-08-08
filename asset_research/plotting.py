import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import numpy as np
import pandas as pd
import json
from plotly.subplots import make_subplots

pio.renderers.default = "browser"


# orderbook related plot
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


def orderbook_heatmap(orderbook_df, code=None, freq='1T'):
    if code is not None:
        orderbook_df = orderbook_df[orderbook_df['code'] == code]
    orderbook_df['svr_recv_time_ask'] = pd.to_datetime(orderbook_df['svr_recv_time_ask'])
    orderbook_df['svr_recv_time_bid'] = pd.to_datetime(orderbook_df['svr_recv_time_bid'])
    orderbook_df = orderbook_df.dropna(subset=['svr_recv_time_ask', 'svr_recv_time_bid'])  # type:pd.DataFrame
    # how to aggregate the map
    orderbook_df['time_key'] = np.where(orderbook_df['svr_recv_time_ask'] > orderbook_df['svr_recv_time_bid'],
                                        orderbook_df['svr_recv_time_ask'], orderbook_df['svr_recv_time_bid'])
    orderbook_df = orderbook_df[['time_key', 'Bid', 'Ask']]
    orderbook_df.set_index('time_key', inplace=True)

    prices = np.array(orderbook_df["Bid"].agg(lambda x: np.array(x)[:, 0]).to_list()).flatten()
    prices = np.append(prices, np.array(orderbook_df["Ask"].agg(lambda x: np.array(x)[:, 0]).to_list()).flatten())
    prices = np.unique(prices)

    grouped = orderbook_df.groupby(pd.Grouper(freq=freq))['Bid', 'Ask'].agg(lambda x: np.sum(x))
    grouped = grouped[grouped['Bid'] != 0]
    grouped = grouped[grouped['Ask'] != 0]

    def col_func(x):
        a = np.array(x)
        count, value = np.histogram(a[:, 0], bins=prices, weights=a[:, 1])
        count2, value = np.histogram(a[:, 0], bins=prices)
        count = np.where(count == 0, np.NAN, count / count2)
        return count

    grouped['Bid'] = grouped['Bid'].apply(lambda x: col_func(x))
    grouped['Ask'] = grouped['Ask'].apply(lambda x: col_func(x))

    # print(grouped['Ask'].index)
    bid = go.Heatmap(
        z=np.array(grouped['Bid'].to_list()), zmin=0, zmax=10,
        x=grouped['Bid'].index,
        y=prices, transpose=True,
        colorscale='Greens', showscale=False)

    ask = go.Heatmap(
        z=np.array(grouped['Ask'].to_list()), zmin=0, zmax=10,
        x=grouped['Ask'].index,
        y=prices, transpose=True,
        colorscale='Reds', showscale=False, )

    fig = go.Figure([bid, ask])
    fig.update_layout(template='plotly_dark', yaxis_tickformat='g')
    # fig.show()

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


def cumulative_volume(rt_df):
    grouped_rt = rt_df.groupby(['ticker_direction', 'price']).agg({'volume': 'sum'}).reset_index()
    neutral = grouped_rt[grouped_rt['ticker_direction'] == 'NEUTRAL']
    buy = grouped_rt[grouped_rt['ticker_direction'] == 'BUY']
    sell = grouped_rt[grouped_rt['ticker_direction'] == 'SELL']
    neutral_bar = go.Bar(
        x=neutral['volume'],
        y=neutral['price'],
        text=neutral['volume'],
        textposition='auto',
        orientation='h', name='Neutral', marker=dict(
            color='grey', ), )
    buy_bar = go.Bar(
        x=buy['volume'],
        y=buy['price'],
        text=buy['volume'],
        textposition='auto',
        orientation='h', name='Buy', marker=dict(
            color='green', ), )
    sell_bar = go.Bar(
        x=sell['volume'],
        y=sell['price'],
        text=sell['volume'],
        textposition='auto',
        orientation='h', name='Sell', marker=dict(
            color='red', ), )

    fig = go.Figure(data=[neutral_bar, buy_bar, sell_bar])
    fig.update_layout(barmode='stack', template='plotly_dark', yaxis_tickformat='g')
    fig.show()
    return fig


def order_flow_plot(tick_df, freq='1T'):
    # template = 'plotly_dark'

    # fig.add_trace(go.Violin(x=df['day'][df['smoker'] == 'Yes'],
    #                         y=df['total_bill'][df['smoker'] == 'Yes'],
    #                         legendgroup='Yes', scalegroup='Yes', name='Yes',
    #                         side='negative',
    #                         line_color='blue')
    #               )

    vol_df = tick_df.groupby(['time', 'ticker_direction', 'price']).agg({'volume': 'sum'})
    sell_to_bid = vol_df.loc[(slice(None), ['SELL']), :]
    sell_to_bid = sell_to_bid.unstack()
    sell_to_bid = sell_to_bid.groupby(pd.Grouper(freq=freq, level=0)).sum()
    sell_to_bid['ticker_direction'] = 'SELL'

    buy_by_ask = vol_df.loc[(slice(None), ['BUY']), :]
    buy_by_ask = buy_by_ask.unstack()
    buy_by_ask = buy_by_ask.groupby(pd.Grouper(freq=freq, level=0)).sum()
    buy_by_ask['ticker_direction'] = 'BUY'

    orderflow_table = buy_by_ask.append(sell_to_bid).replace(np.NAN, 0)
    orderflow_table = orderflow_table.set_index('ticker_direction', append=True).sort_index()

    v = orderflow_table.values
    a = np.empty(v.shape, dtype='bool')
    for i in range(len(v)):
        nonzero_idx = np.nonzero(v[i])[0]
        c = v[i] != 0
        try:
            c[nonzero_idx[0]: nonzero_idx[-1]] = True
        except:
            pass
        a[i] = c

    orderflow_table.where(a, None, inplace=True)
    orderflow_table = orderflow_table.T.droplevel(0).sort_index(ascending=False).sort_index(axis=1,
                                                                                            ascending=[True, False])
    colorscale = [[0, '#CE0000'],
                  [0.1, '#EA0000'],
                  [0.2, '#FF2D2D'],
                  [0.3, '#FF7575'],
                  [0.4, '#FF9797'],
                  [0.5, '#FFFFFF'],
                  [0.6, '#02DF82'],
                  [0.7, '#01B468'],
                  [0.8, '#019858'],
                  [0.9, '#01814A'],
                  [1, '#006030']

                  ]
    # of_heatmap = ff.create_annotated_heatmap(z=orderflow_table, zmin=-10, zmax=10,)
    of_heatmap = go.Heatmap(
        z=orderflow_table, zmin=-10, zmax=10,
        x=orderflow_table.columns,
        y=orderflow_table.index,
        colorscale=colorscale, showscale=False, text=orderflow_table)
    fig = go.Figure(of_heatmap)
    return fig


    pass


def bid_ask_plot():
    pass


def triple_screen_plot():
    pass


if __name__ == '__main__':
    # sample = {'_id': {'$oid': '5f22eac623de44d2b46056ce'},
    #           'code': 'HK.999010',
    #           'svr_recv_time_bid': '2020-07-30 23:44:06.596',
    #           'svr_recv_time_ask': '2020-07-30 23:44:06.596',
    #           'Bid': [[24476.0, 1, 1],
    #                   [24475.0, 4, 3],
    #                   [24474.0, 2, 2],
    #                   [24473.0, 4, 4],
    #                   [24472.0, 3, 3],
    #                   [24471.0, 2, 2],
    #                   [24470.0, 8, 3],
    #                   [24469.0, 3, 3],
    #                   [24468.0, 2, 2],
    #                   [24467.0, 3, 3]],
    #           'Ask': [[24477.0, 1, 1],
    #                   [24478.0, 2, 2],
    #                   [24479.0, 4, 4],
    #                   [24480.0, 2, 2],
    #                   [24481.0, 4, 4],
    #                   [24482.0, 3, 3],
    #                   [24483.0, 5, 5],
    #                   [24484.0, 4, 4],
    #                   [24485.0, 7, 5],
    #                   [24486.0, 3, 3]]}
    # # orderbook_plot(sample).show()
    rt_df = pd.read_csv('2020-07-30.csv')
    rt_df = rt_df[rt_df['code'] == 'HK.999010']
    rt_df['time'] = pd.to_datetime(rt_df['time'])
    rt_df['hours'] = rt_df['time'].apply(lambda x: x.hour)

    rt_df = rt_df[(rt_df['hours'] >= 9) & (rt_df['hours'] <= 12)]
    # tick_plot(rt_df)
    # cumulative_volume(rt_df)
    # order_flow_plot(rt_df)

    vol_df = rt_df.groupby(['time', 'ticker_direction', 'price']).agg({'volume': 'sum'})
    # vol_df['time'] = pd.to_datetime(vol_df['time'])
    # prices = vol_df['price'].unique()
    # prices.sort()
    sell_to_bid = vol_df.loc[(slice(None), ['SELL']), :]
    sell_to_bid = sell_to_bid.unstack()
    sell_to_bid = sell_to_bid.groupby(pd.Grouper(freq='30S', level=0)).sum()
    sell_to_bid = -sell_to_bid
    sell_to_bid['ticker_direction'] = 'SELL'

    buy_by_ask = vol_df.loc[(slice(None), ['BUY']), :]
    buy_by_ask = buy_by_ask.unstack()
    buy_by_ask = buy_by_ask.groupby(pd.Grouper(freq='30S', level=0)).sum()
    buy_by_ask['ticker_direction'] = 'BUY'

    orderflow_table = sell_to_bid.append(buy_by_ask).replace(np.NAN, 0)
    orderflow_table = orderflow_table.set_index('ticker_direction', append=True).sort_index()

    v = orderflow_table.values
    a = np.empty(v.shape, dtype='bool')
    for i in range(len(v)):
        nonzero_idx = np.nonzero(v[i])[0]
        c = v[i] != 0
        try:
            c[nonzero_idx[0]: nonzero_idx[-1]] = True
        except:
            print(nonzero_idx)
        a[i] = c


    orderflow_table.where(a, None, inplace=True)
    orderflow_table = orderflow_table.T.droplevel(0).sort_index(ascending=False).sort_index(axis=1,
                                                                                            ascending=[True, False])
    colorscale = [[0, '#CE0000'],
                  [0.1, '#EA0000'],
                  [0.2, '#FF2D2D'],
                  [0.3, '#FF7575'],
                  [0.4, '#FF9797'],
                  [0.5, '#FFFFFF'],
                  [0.6, '#02DF82'],
                  [0.7, '#01B468'],
                  [0.8, '#019858'],
                  [0.9, '#01814A'],
                  [1, '#006030']

                  ]
    # of_heatmap = ff.create_annotated_heatmap(z=orderflow_table, zmin=-10, zmax=10,)
    of_heatmap = go.Heatmap(
        z=orderflow_table, zmin=-10, zmax=10,
        x=orderflow_table.columns,
        y=orderflow_table.index,
        colorscale=colorscale, showscale=False, text=orderflow_table)

    fig = go.Figure(of_heatmap)
    fig.update_layout(template='plotly_dark', yaxis_tickformat='g')
    fig.show()
    # table = go.Table(
    #
    #     header=dict(values=orderflow_table.columns),
    #     cells=dict(values=orderflow_table.values.T)
    #
    # )
    #
    # fig = go.Figure([table])
    # fig.show()
    # records = []
    # with open('2020-07-31.json', 'r') as file:
    #     for line in file.readlines():
    #         dic = json.loads(line)
    #         records.append(dic)
    # df = pd.DataFrame(records)[-30000:]
    #
    # orderbook_df = df[df['code'] == 'HK.999010'].drop('_id', axis=1)
    #
    # orderbook_heatmap(orderbook_df, freq='5s')
