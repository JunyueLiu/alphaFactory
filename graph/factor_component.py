from plotly import graph_objects as go
import pandas as pd


def line(data: pd.DataFrame or pd.Series, timestamp=None, name=None, mode='lines', color=None, strftime_format = '%Y/%m/%d %H:%M:%S'):
    if timestamp is None:
        timestamp = data.index
        timestamp = timestamp.strftime(strftime_format)
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, strftime_format))
    elif isinstance(timestamp, pd.DatetimeIndex):
        timestamp = timestamp.strftime(strftime_format)

    return go.Scatter(x=timestamp, y=data.values,
                      mode=mode, line_color=color,
                      name=name)


def histogram(factor: pd.DataFrame or pd.Series):
    return go.Histogram(x=factor, histnorm='probability')


def heatmap(x, y, z):
    return go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale='Viridis')
