from plotly import graph_objects as go
import pandas as pd


def line(factor: pd.DataFrame, name = None):
    return go.Scatter(x=factor.index, y=factor.values,
                      mode='lines',
                      name=name)


def histogram(factor: pd.DataFrame):
    return go.Histogram(x=factor, histnorm='probability')


def heatmap(x, y, z):
    return go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale='Viridis')
