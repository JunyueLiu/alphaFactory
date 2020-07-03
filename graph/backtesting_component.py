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
        return '%Y/%m/%d %H:%M:%S'
    else:
        return '%Y/%m/%d'


def net_value_line(net_value: pd.Series, color='#00477D', name='net value', fill=None):
    strftime_format = _infer_strftime_format(net_value.index)
    timestamp = net_value.index  # type:pd.DatetimeIndex
    timestamp = timestamp.strftime(strftime_format)
    return go.Scatter(x=timestamp, y=net_value.values,
                      mode='lines', line_color=color,
                      name=name, fill=fill)


def returns_distribution(returns: pd.DataFrame or pd.Series):
    return go.Histogram(x=returns)


def entry_exit_dot(traded: pd.DataFrame, long=True, long_marker='#3283FE', short_marker='#FF0000'):
    traded_time = traded['update_time'].apply(lambda x: x.replace('-', '/'))
    traded_price = traded['dealt_price']
    if 'remarks' in traded.columns:
        hover_text = traded.apply(lambda x: 'deal time: {} <br>deal price: {} <br>deal qty: {} <br>'
                                            'direction: {} <br>remarks: {}'
                                  .format(x['update_time'], x['dealt_price'], x['dealt_qty'], x['order_direction'],
                                          x['remarks']),
                                  axis=1)
    else:
        hover_text = traded.apply(lambda x: 'deal time: {} <br>deal price: {} <br>deal qty: {} <br>'
                                            'direction: {}'
                                  .format(x['update_time'], x['dealt_price'], x['dealt_qty'], x['order_direction']),
                                  axis=1)

    if long:
        dot = go.Scatter(x=traded_time, y=traded_price,
                         mode='markers', name='long', hovertext=hover_text, marker_color=long_marker, marker_size=8)
    else:
        dot = go.Scatter(x=traded_time, y=traded_price,
                         mode='markers', name='short', hovertext=hover_text, marker_color=short_marker, marker_size=8)
    return dot


def entrust_dot(traded: pd.DataFrame, long=True, long_marker='#30D5C8', short_marker='#FF0DA6'):
    order_time = traded['order_time'].apply(lambda x: x.replace('-', '/'))
    order_price = traded['order_price']
    if 'remarks' in traded.columns:
        hover_text = traded.apply(lambda x: 'order time: {} <br>order price: {} <br>order qty: {} <br>'
                                            'direction: {} <br>remarks: {}'
                                  .format(x['order_time'], x['order_price'], x['order_qty'], x['order_direction'],
                                          x['remarks']),
                                  axis=1)
    else:
        hover_text = traded.apply(lambda x: 'order time: {} <br>order price: {} <br>order qty: {} <br>'
                                            'direction: {}'
                                  .format(x['order_time'], x['order_price'], x['order_qty'], x['order_direction']),
                                  axis=1)

    if long:
        dot = go.Scatter(x=order_time, y=order_price,
                         mode='markers', name='long entrust', hovertext=hover_text, marker_color=long_marker,
                         marker_size=4)
    else:
        dot = go.Scatter(x=order_time, y=order_price,
                         mode='markers', name='short entrust', hovertext=hover_text, marker_color=short_marker,
                         marker_size=4)
    return dot
