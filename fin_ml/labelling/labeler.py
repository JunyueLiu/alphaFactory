# TRIPLE - BARRIER LABELING METHOD
import pandas as pd
import numpy as np
import tqdm
from collections import Counter


def getDailyVol(df, span0=100):
    # return
    df['return'] = df.groupby(['code'])['close'].apply(lambda x: x / x.shift(1) - 1)
    # estimated volatility
    sigma = df.groupby(['code'])['return'].apply(lambda x: x.ewm(span=span0).std())
    return sigma


def TBL(df, barrier, width):
    upwidth, downwidth = width
    barrier_ = barrier
    result = barrier_[['code', 'time_key', 'vb']].copy(deep=True)
    if upwidth > 0:
        barrier_['ub'] = upwidth * barrier_['volume']
    else:
        barrier_['ub'] = np.nan
    if downwidth > 0:
        barrier_['db'] = -downwidth * barrier_['volume']
    else:
        barrier_['db'] = np.nan
    for code in barrier_.code.unique():
        barrier0 = barrier_[barrier_.code == code]
        print(barrier0)
        for col, time_key, vb in barrier_[['time_key', 'vb']].itertuples():
            df0 = df[(df.time_key > time_key) & (df.time_key < vb)]
            df0['return'] = df0['close'] / df[df.time_key == time_key]['close'].iloc[0] - 1
            result.loc[result.index[(result.time_key == time_key) & (result.code == code)], 'ut'] = \
                df0[df0['return'] > barrier0[barrier0.time_key == time_key]['ub'].iloc[0]]['time_key'].min()
            result.loc[result.index[(result.time_key == time_key) & (result.code == code)], 'dt'] = \
                df0[df0['return'] < barrier0[barrier0.time_key == time_key]['db'].iloc[0]]['time_key'].min()
    return result


def get_first_touch(df, barrier, width):
    result = TBL(df, barrier, width)
    result['first'] = result[['vb', 'ut', 'dt']].dropna(how='all').min(axis=1)
    return result


def get_bins(result, df):
    result = result.dropna(subset=['first'])
    out = result[['code', 'time_key']]
    barprice = pd.merge(result, df, on=['code', 'time_key'], how='left')['close']
    touchprice = pd.merge(result, df, left_on=['code', 'first'], right_on=['code', 'time_key'], how='left')['close']
    out['ret'] = touchprice / barprice - 1
    out['bin'] = np.sign(out['ret'])
    return out


def triple_barrier_label(candles: pd.DataFrame,
                         upper: float or list or np.array,
                         lower: float or list or np.array,
                         right: int or list or np.array,
                         event: list or np.array or None = None) -> pd.Series:
    if event is None:
        event = candles.index.values
    # check if legal
    if isinstance(upper, float) is False:
        if len(upper) != len(event):
            raise ValueError(
                'upper list must have same length with event, but upper has lenght of {}, event has length of {}'.format(
                    len(upper), len(event)))
    else:
        upper = candles.loc[event]['close'] * (1 + upper)

    if isinstance(lower, float) is False:
        if len(lower) != len(event):
            raise ValueError(
                'lower list must have same length with event, but lower has lenght of {}, event has length of {}'.format(
                    len(lower), len(event)))
    else:
        lower = candles.loc[event]['close'] * (1 - lower)

    if isinstance(right, int) is False:
        if len(right) != len(event):
            raise ValueError(
                'right list must have same length with event, but right has lenght of {}, event has length of {}'.format(
                    len(lower), len(event)))
        if isinstance(right[0], (int, np.int64, np.int, np.int32, np.int16)):
            r = []
            for i in range(len(event)):
                future = candles.loc[event[i]:]
                try:
                    future = future.iloc[right[i]].name
                    r.append(future)
                except:
                    pass
            right = np.array(r)
        elif isinstance(right[0], pd.Timestamp):
            right_is_future = np.all(right > event)
            if right_is_future is False:
                raise ValueError('right larger than event date')
    else:
        right = pd.Series(candles.index, index=candles.index).shift(-right)[event].dropna().values
    label = []
    for i in tqdm.tqdm(range(0, len(right))):
        label_data = candles.loc[event[i]: right[i]]
        counter = 0
        for idx, row in label_data.iterrows():
            upper_barrier = upper[i]
            lower_barrier = lower[i]

            if row['high'] >= upper_barrier:
                if row['low'] <= lower_barrier:
                    # touch both and same time, label 3
                    # print(row, upper_barrier, lower_barrier)
                    label.append(3)
                else:
                    # touch up, label 2
                    label.append(2)
                break
            elif row['low'] <= lower_barrier:
                # touch low, label0
                label.append(0)
                break
            elif counter == len(label_data) - 1:
                # no touch the whole period
                label.append(1)
            counter += 1

    print('\nfinish labelling, result: ', Counter(label))
    return pd.Series(label, index=event[:len(right)], name='label')
