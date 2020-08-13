import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio

pio.renderers.default = "browser"

from asset_research.utils import get_orderbook_df


def realtime_orderbook_heatmap(orderbook_df, code=None, ):
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
    best_bid = orderbook_df['Bid'].apply(lambda x: x[0][0])
    best_ask = orderbook_df['Ask'].apply(lambda x: x[0][0])
    prices = np.array(orderbook_df["Bid"].agg(lambda x: np.array(x)[:, 0]).to_list()).flatten()
    prices = np.append(prices, np.array(orderbook_df["Ask"].agg(lambda x: np.array(x)[:, 0]).to_list()).flatten())
    prices = np.unique(prices)

    grouped = orderbook_df

    def col_func(x):
        a = np.array(x)
        count, value = np.histogram(a[:, 0], bins=prices, weights=a[:, 1])
        c = count != 0
        nonzero = count.nonzero()[0]
        c[nonzero[0]: nonzero[-1]] = True
        count = np.where(c, count, np.NAN)
        return count

    grouped['Bid'] = grouped['Bid'].apply(lambda x: col_func(x))
    grouped['Ask'] = grouped['Ask'].apply(lambda x: col_func(x))
    now = grouped.index[-1]
    idx = pd.date_range(now, periods=60, freq='s')

    future = pd.DataFrame(np.repeat(grouped.iloc[-1].values, 60, axis=0).reshape(2, 60).T, index=idx,
                          columns=grouped.columns)
    grouped = grouped.append(future)

    last_bid = best_bid.iloc[-1]
    last_ask = best_ask.iloc[-1]
    fb = pd.Series(np.repeat(last_bid, 60), index=idx)
    fa = pd.Series(np.repeat(last_ask, 60), index=idx)
    best_bid = best_bid.append(fb)
    best_ask = best_ask.append(fa)

    best_bid_plot = go.Scatter(x=best_bid.index, y=best_bid.values, mode='lines', line_color='#00FF00', line_width=6)
    best_ask_plot = go.Scatter(x=best_ask.index, y=best_ask.values, mode='lines', line_color='#FF0000', line_width=6)

    bid = go.Heatmap(
        z=np.array(grouped['Bid'].to_list()), zmin=0, zmax=10,
        x=grouped['Bid'].index,
        y=prices, transpose=True,
        colorscale='magma', showscale=False)

    ask = go.Heatmap(
        z=np.array(grouped['Ask'].to_list()), zmin=0, zmax=10,
        x=grouped['Ask'].index,
        y=prices, transpose=True,
        colorscale='magma', showscale=False, )

    fig = go.Figure([bid, ask, best_bid_plot, best_ask_plot])
    fig.update_layout(yaxis_tickformat='g')
    fig.update_layout(
        shapes=[dict(
            x0=now, x1=now, y0=0, y1=1, xref='x', yref='paper',
            line_width=2)],
        annotations=[dict(
            x=now, y=0.05, xref='x', yref='paper',
            showarrow=False, xanchor='left', text='Live')]
    )
    # fig.show()

    return fig


if __name__ == '__main__':
    ob_df = get_orderbook_df('/Users/liujunyue/PycharmProjects/alphaFactory/asset_research/2020-07-31.json')
    ob_df = ob_df[1000: 1500]
    realtime_orderbook_heatmap(ob_df, code='HK.999010').show()
