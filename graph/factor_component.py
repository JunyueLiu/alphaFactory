from plotly import graph_objects as go
import pandas as pd

def histogram(factor:pd.DataFrame):
    return go.Histogram(x=factor)

def heatmap(x, y, z):
    return go.Heatmap(
        z=z,
        x=x,
        y=y,
        colorscale='Viridis')