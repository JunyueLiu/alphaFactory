from plotly import graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats


def _infer_strftime_format(data: pd.DatetimeIndex):
    unique_index = np.unique(data.values)
    unique_index.sort()
    time_delta = unique_index[1:] - unique_index[:-1]
    # get mode using scipy
    td = stats.mode(time_delta)[0][0]
    td = td.astype('timedelta64[m]')

    day = td / np.timedelta64('1', 'D')

    if day < 1:
        return '%Y-%m-%d %H:%M:%S'
    else:
        return '%Y-%m-%d'


def net_value_line(net_value: pd.Series, color='#00477D', name='net value'):
    strftime_format = _infer_strftime_format(net_value.index)
    timestamp = net_value.index  # type:pd.DatetimeIndex
    timestamp = timestamp.strftime(strftime_format)
    return go.Scatter(x=timestamp, y=net_value.values,
                      mode='lines', line_color=color,
                      name=name)


def returns_distribution(returns: pd.DataFrame or pd.Series):
    return go.Histogram(x=returns)


def entry_exit_dot(traded_time: pd.Series, traded_price, long=True):
    traded_time = traded_time.copy().apply(lambda x: x.replace('-', '/'))
    if long:

        dot = go.Scatter(x=traded_time, y=traded_price,
                         mode='markers', name='long', marker_color='#000080')
    else:
        dot = go.Scatter(x=traded_time, y=traded_price,
                         mode='markers', name='long', marker_color='#FF0000')
    return dot
