import numpy as np
from graph.factor_component import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots



def price_factor_plot(data:pd.DataFrame, factor, price_key = 'close', price_name = 'close', factor_name = 'factor'):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(line(data[price_key], price_name), secondary_y=False)
    fig.add_trace(line(factor, factor_name), secondary_y=True)
    fig.update_layout(
        title_text=""
    )

    # Set x-axis title
    fig.update_xaxes(title_text="time")

    # Set y-axes titles
    fig.update_yaxes(title_text=price_name, secondary_y=False)
    fig.update_yaxes(title_text=factor_name, secondary_y=True)
    return fig


def returns_plot(factor_returns, factor_name = None):
    fig = go.Figure()
    fig.add_trace(line(factor_returns, factor_name))
    return fig

def cumulative_return(cumulative_factor_returns, benchmark = None, factor_name = 'factor', benchmark_name=None):
    fig = go.Figure()
    fig.add_trace(line(cumulative_factor_returns, factor_name))
    if benchmark:
        fig.add_trace(line(benchmark, benchmark_name))
    return fig

def factor_distribution_plot(factor):
    fig = go.Figure()
    fig.add_trace(histogram(factor))
    return fig

