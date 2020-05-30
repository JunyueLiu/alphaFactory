import plotly.graph_objects as go
import pandas as pd


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


