import numpy as np
from scipy import stats
from graph.factor_component import *
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def price_factor_plot(data: pd.DataFrame, factor: pd.Series, price_key='close', price_name='close',
                      factor_name='factor'):
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # timestamp = data.index
    fig.add_trace(line(factor, name=factor_name, color='#FFBF00'), secondary_y=True)
    fig.add_trace(line(data[price_key], name=price_name, color='#008000'), secondary_y=False)
    fig.update_layout(
        title_text=""
    )
    # Set x-axis title
    fig.update_xaxes(title_text="time")

    # Set y-axes titles
    fig.update_yaxes(title_text=price_name,
                     range=[data[price_key].min() * 0.99, data[price_key].max() * 1.01],
                     secondary_y=False)
    fig.update_yaxes(title_text=factor_name, secondary_y=True)
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False, yaxis_tickformat='g')
    return fig


def returns_plot(factor_returns, factor_name='factor'):
    fig = go.Figure()
    for col in factor_returns.columns:
        fig.add_trace(line(factor_returns[col], name=factor_name + '_' + col))
    fig.update_layout(yaxis_tickformat='g')
    return fig


def cumulative_return_plot(cumulative_factor_returns, benchmark=None, factor_name='factor', benchmark_name='benchmark'):
    fig = go.Figure()
    for col in cumulative_factor_returns.columns:
        fig.add_trace(line(cumulative_factor_returns[col], name=factor_name + '_' + col))
    if benchmark is not None:
        fig.add_trace(line(benchmark, name=benchmark_name, color='#008000'))
    return fig


def factor_distribution_plot(factor):
    fig = go.Figure()
    fig.add_trace(histogram(factor))
    return fig


def entry_and_exit_plot(data: pd.DataFrame, factor, price_key='close'):
    fig = go.Figure()
    fig.add_trace(line(data[price_key], name=price_key, color='grey'))
    long = pd.Series(np.where(factor == 1, data[price_key], np.nan), index=data.index)
    short = pd.Series(np.where(factor == -1, data[price_key], np.nan), index=data.index)

    fig.add_trace(line(long, name='long', color='green'))
    fig.add_trace(line(short, name='short', color='red'))

    fig.update_layout(yaxis_tickformat='g')
    return fig

def qq_plot(factor:pd.DataFrame):
    # stats.probplot()
    factor = factor.dropna()
    qq = stats.probplot(factor, dist='norm', sparams=(1, ))
    x = np.array([qq[0][0][0], qq[0][0][-1]])
    fig = go.Figure()
    pts = go.Scatter(x=qq[0][0],
                     y=qq[0][1],
                     mode='markers',
                     showlegend=False
                     )
    line = go.Scatter(x=x,
                      y=qq[1][1] + qq[1][0] * x,
                      showlegend=False,
                      mode='lines'
                      )
    fig.add_trace(pts)
    fig.add_trace(line)
    fig.update_xaxes(title_text="Normal Distribution Quantile")
    fig.update_yaxes(title_text="Factor Observed Quantile")
    return fig


def report_plot():
    pass