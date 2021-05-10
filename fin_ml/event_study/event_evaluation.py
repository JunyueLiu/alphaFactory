import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from db_wrapper.mongodb_utils import MongoConnection
from fin_ml.event_study.technical_events import sma_cross_up_event


def event_future_return(ohlc: pd.DataFrame, events: pd.Series):
    merged = ohlc.join(events)
    stats = {}
    fig = make_subplots(rows=5, cols=4, shared_xaxes=True, )
    for t in range(1, 21):
        merged['forward_ret_{}'.format(t)] = np.log(merged['close'].shift(-t) / merged['close'])
        # todo return in term of ATR
        fr = merged[(merged[events.name] != 0) & (merged[events.name].isna() == False)]['forward_ret_{}'.format(t)]
        s_df = fr.describe()
        pnl = fr * merged[(merged[events.name] != 0) & (merged[events.name].isna() == False)][events.name]
        win_ratio = len(pnl[pnl > 0]) / len(pnl)
        s_df['win ratio'] = win_ratio
        s_df['t-stats'] = s_df['mean'] / s_df['std']
        stats['forward_ret_{}'.format(t)] = s_df
        i = (t - 1) // 4 + 1
        j = t - 4 * ((t - 1) // 4)

        sub_fig = ff.create_distplot([pnl.dropna()], ['forward_ret_{}'.format(t)], bin_size=0.001,
                                     colors=[px.colors.qualitative.Alphabet[t % 26]]
                                     )
        for g in sub_fig.data:
            fig.add_trace(g, row=i, col=j)

    stats = pd.DataFrame(stats)
    return stats, fig


def did_study(ohlc: pd.DataFrame, events: pd.Series):
    merged = ohlc.join(events)
    stats = {}
    fig = make_subplots(rows=5, cols=4, shared_xaxes=True, )
    for t in range(1, 21):
        merged['forward_ret_{}'.format(t)] = np.log(merged['close'].shift(-t) / merged['close'])
        merged['backward_ret_{}'.format(t)] = np.log(merged['close'] / merged['close'].shift(t))
        merged['diff_{}'.format(t)] = merged['forward_ret_{}'.format(t)] - merged['backward_ret_{}'.format(t)]
        # todo return in term of ATR
        fr = merged[(merged[events.name] != 0) & (merged[events.name].isna() == False)]['diff_{}'.format(t)]
        s_df = fr.describe()
        pnl = fr * merged[(merged[events.name] != 0) & (merged[events.name].isna() == False)][events.name]
        win_ratio = len(pnl[pnl > 0]) / len(pnl)
        s_df['win ratio'] = win_ratio
        s_df['t-stats'] = s_df['mean'] / s_df['std']
        stats['forward_ret_{}'.format(t)] = s_df
        i = (t - 1) // 4 + 1
        j = t - 4 * ((t - 1) // 4)

        sub_fig = ff.create_distplot([pnl.dropna()], ['diff_{}'.format(t)], bin_size=0.001,
                                     colors=[px.colors.qualitative.Alphabet[t % 26]]
                                     )
        for g in sub_fig.data:
            fig.add_trace(g, row=i, col=j)

    stats = pd.DataFrame(stats)
    return stats, fig


if __name__ == '__main__':
    con = MongoConnection('localhost')
    ohlc = con.get_ohlc_arctic('3000count', 'EUR/USD')
    events = sma_cross_up_event(ohlc, 5, 10)
    stats, fig = event_future_return(ohlc, events)
    fig.write_html('future_ret.html')
    stats1, fig2 = did_study(ohlc, events)
    fig2.write_html('did.html')
