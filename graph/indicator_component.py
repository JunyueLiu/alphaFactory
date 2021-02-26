import numpy as np
import plotly.graph_objects as go
import pandas as pd

from graph import green, red, blue
from technical_analysis.momentum import *
from technical_analysis.overlap import *
import plotly.io as pio

pio.renderers.default = "browser"


def volume(df: pd.DataFrame, timestamp=None, volume_key='volume'):
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))
    return go.Bar(x=timestamp, y=df[volume_key], name=volume_key)


def band2(df: pd.DataFrame, timestamp=None, band_key=None, color=None, mode='lines'):
    if band_key is None:
        band_key = ['up', 'down']

    if color is None:
        color = ['#00FF00', '#FF0000']
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))

    up = go.Scatter(x=timestamp, y=df[band_key[0]], mode=mode, line_color=color[0])
    down = go.Scatter(x=timestamp, y=df[band_key[1]], mode=mode, line_color=color[1])
    return up, down


def band3(df: pd.DataFrame, timestamp=None, band_key=None, color=None, mode='lines'):
    if band_key is None:
        band_key = ['up', 'mid', 'down']

    if color is None:
        color = ['#FFFF00', '#00FFFF', '#FF00FF']
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))

    up = go.Scatter(x=timestamp, y=df[band_key[0]], mode=mode, line_color=color[0], name=band_key[0])
    mid = go.Scatter(x=timestamp, y=df[band_key[1]], mode=mode, line_color=color[1], name=band_key[1])
    down = go.Scatter(x=timestamp, y=df[band_key[2]], mode=mode, line_color=color[2], name=band_key[2])
    return up, mid, down


def no_overlap(df: pd.DataFrame, timestamp=None, band_key=None, color=None, mode='lines'):
    lines = []
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))

    for key in band_key:
        if color is not None:
            line = go.Scatter(x=timestamp, y=df[key], mode=mode, name=key, line_color=color[key])
        else:
            line = go.Scatter(x=timestamp, y=df[key], mode=mode, name=key)
        lines.append(line)
    return lines


def macd_graph(df: pd.DataFrame, timestamp=None, macd_keys=None, color=None):
    if color is None:
        color = ['#FF8000', '#2894FF', '#FF2D2D', '#02C874']
    if macd_keys is None:
        macd_keys = ['macd', 'macdsignal', 'macdhist']

    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    elif isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))
    else:
        raise NotImplementedError

    marker_color = np.where(df[macd_keys[2]] < 0, color[2], color[3])

    fast = go.Scatter(x=timestamp, y=df[macd_keys[0]], name=macd_keys[0], mode='lines', line_color=color[0])
    slow = go.Scatter(x=timestamp, y=df[macd_keys[1]], name=macd_keys[1], mode='lines', line_color=color[1])
    hist_ = go.Bar(x=timestamp, y=df[macd_keys[2]], name=macd_keys[2], marker_color=marker_color)
    return [fast, slow, hist_]


def sar_graph(series: pd.Series, close: pd.Series or None = None, timestamp=None, color=None):
    if color is None:
        color = [red, green, blue]

    if timestamp is None:
        timestamp = series.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    elif isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))
    else:
        raise NotImplementedError
    if close is None:
       marker_color = [blue] * len(series)
    else:
        marker_color = np.where(series < close, color[1], color[0])
    return go.Scatter(x=timestamp, y=series, name='SAR', mode='markers', marker_color=marker_color)

def pattern_graph(series: pd.Series, timestamp=None, direction=None, annotation=None):

    pass







if __name__ == '__main__':
    df = pd.read_csv('../local_data/EURUSD/count5000.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df[:100]
    go.Figure(macd_graph(MACDFIX(df))).show()
    go.Figure(sar_graph(SAREXT(df),df['close'])).show()