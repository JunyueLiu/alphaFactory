import numpy as np
import pandas as pd
import plotly.graph_objects as go
from arctic import Arctic
import plotly.io as pio
from plotly.validators.scatter.marker import SymbolValidator

from graph import green, red, blue, purple
from graph.utils import timestamp_parser
from technical_analysis.channel import Bollinger_bands, Bollinger_Donchian
from technical_analysis.momentum import *
from technical_analysis.overlap import *

pio.renderers.default = "browser"


def volume(df: pd.DataFrame, timestamp=None, volume_key='volume'):
    """

    :param df:
    :param timestamp:
    :param volume_key:
    :return:
    """
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))
    return go.Bar(x=timestamp, y=df[volume_key], name=volume_key)


def band2(df: pd.DataFrame, timestamp=None, band_key=None, color=None, mode='lines'):
    """

    :param df:
    :param timestamp:
    :param band_key:
    :param color:
    :param mode:
    :return:
    """
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
    """

    :param df:
    :param timestamp:
    :param band_key:
    :param color:
    :param mode:
    :return:
    """
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
    down = go.Scatter(x=timestamp, y=df[band_key[2]], mode=mode, line_color=color[2], name=band_key[2], fill='tonexty',
                      fillcolor='rgba(0,153,0,0.1)')
    mid = go.Scatter(x=timestamp, y=df[band_key[1]], mode=mode, line_color=color[1], name=band_key[1], fill='tonexty',
                     fillcolor='rgba(0,153,0,0.1)')
    return up, mid, down


def no_overlap(df: pd.DataFrame, timestamp=None, band_key=None, color=None, mode='lines'):
    """

    :param df:
    :param timestamp:
    :param band_key:
    :param color:
    :param mode:
    :return:
    """
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
    """

    :param df:
    :param timestamp:
    :param macd_keys:
    :param color:
    :return:
    """

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
    """

    :param series:
    :param close:
    :param timestamp:
    :param color:
    :return:
    """
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


def rsi_graph(series: pd.Series, timestamp=None, overbuy=80, oversell=20):
    """

    :param series:
    :param timestamp:
    :param overbuy:
    :param oversell:
    :return:
    """
    fig = go.Figure()
    x = timestamp_parser(series, timestamp)
    fig.add_scatter(x=x, y=series, name=series.name, mode='line', line_color=purple)
    fig.add_hline(y=50, line_width=3, line_dash='dash', fillcolor=purple)
    fig.add_hrect(y0=oversell, y1=overbuy, line_width=1, line_dash='dash', fillcolor=purple, opacity=0.2)
    return fig.data



def pattern_graph(series: pd.Series, timestamp=None, direction=None, annotation=None):
    pass


def channel_graph(df: pd.DataFrame, timestamp=None):
    band_key = ['upperband', 'middleband', 'lowerband']
    colors = [green, red, green]
    return band3(df, timestamp, band_key, colors)


def event_marker_graph(events: pd.Series, timestamp=None, direction: int = 1):
    timestamp = timestamp_parser(events, timestamp)
    if direction == 1:
        return go.Scatter(x=timestamp, y=events,
                          name=events.name, mode='markers', marker_symbol="triangle-up", marker_color=green,
                          marker_size=15)
    else:
        return go.Scatter(x=timestamp, y=events,
                          name=events.name, mode='markers', marker_symbol="triangle-down", marker_color=red,
                          marker_size=15)


if __name__ == '__main__':
    store = Arctic('localhost')
    df = store['3000count'].read('EUR/USD').data
    df = df[-300:]
    # go.Figure(macd_graph(MACDFIX(df))).show()
    # go.Figure(sar_graph(SAREXT(df), df['close'])).show()
    events = df.sample(10)['close']
    band = Bollinger_Donchian(df)
    u, m, d = channel_graph(band)
    e = event_marker_graph(events, direction=-1)
    go.Figure([u, m, d, e]).show()
