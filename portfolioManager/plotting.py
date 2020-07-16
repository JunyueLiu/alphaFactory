import pandas as pd
from plotly import graph_objects as go
import plotly.figure_factory as ff
from graph.factor_component import line
import numpy as np


def net_values_plot(net_values: pd.DataFrame):
    fig = go.Figure()
    for col in net_values.columns:
        fig.add_trace(line(net_values[col], name=col))
    x_axis = fig.data[0].x
    tick_value = [x_axis[i] for i in range(0, len(x_axis), len(x_axis) // 10)]
    tick_text = [x_axis[i][0:10] for i in range(0, len(x_axis), len(x_axis) // 10)]
    fig.update_xaxes(ticktext=tick_text, tickvals=tick_value, title_text="time")
    fig.update_yaxes(title_text='net value')
    return fig


# rolling correlation?
def rolling_corr(series_1: pd.Series, series_2: pd.Series, windows: int):
    return series_1.rolling(windows).corr(series_2)


# correlation heatmap
def corr_heatmap(corr_matrix: pd.DataFrame):
    x = corr_matrix.columns.to_list()
    y = corr_matrix.index.to_list()
    z = corr_matrix.values
    z_text = np.around(z, decimals=2)

    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis', showscale=True)
    fig.update_layout(dict(plot_bgcolor='#fff',
                           yaxis=dict(
                               showline=False,
                               showgrid=False,
                               zeroline=False,
                               autorange="reversed"),
                           xaxis=dict(
                               showline=False,
                               showgrid=False,
                               zeroline=False

                           )))
    return fig


# return heatmap
def ret_heatmap(net_values: pd.DataFrame, groupby='M'):
    ret = net_values.pct_change().groupby(pd.Grouper(freq=groupby)).sum()
    # todo subplot to better visualization

    x = ret.columns.to_list()
    y = ret.index.to_list()
    z = ret.values
    z_text = np.around(z, decimals=2)

    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale='Viridis', showscale=True)
    fig.update_layout(dict(plot_bgcolor='#fff',
                           yaxis=dict(
                               showline=False,
                               showgrid=False,
                               zeroline=False,
                               autorange="reversed"),
                           xaxis=dict(
                               showline=False,
                               showgrid=False,
                               zeroline=False

                           )))
    return fig


# holding plot
def holding_line_plot(pos: pd.DataFrame, instruments: str, start_date, end_date):
    fig = go.Figure()
    pos_ = pos.loc[(slice(None), instruments), :]  # type: pd.DataFrame
    pos_.index = pos_.index.droplevel(1)
    pos_ = pos_[(pos_.index >= pd.to_datetime(start_date)) & (pos_.index <= pd.to_datetime(end_date))]
    for col in pos_.columns:
        fig.add_trace(line(pos_[col], pos_.index, name=col))
    x_axis = fig.data[0].x
    tick_value = [x_axis[i] for i in range(0, len(x_axis), len(x_axis) // 10)]
    tick_text = [x_axis[i][0:10] for i in range(0, len(x_axis), len(x_axis) // 10)]
    fig.update_xaxes(ticktext=tick_text, tickvals=tick_value, title_text="time")
    fig.update_yaxes(title_text='position')

    return fig


# overall exposure to some asset
## select day and see pie chart
def selected_long_short_pie():
    # todo period is too large for selection

    pass


def efficient_frontier_plot(mean, std,
                            max_sharpe_ret, max_sharpe_std,
                            min_var_ret, min_var_std):
    # todo efficient frontier

    # daily_net = net_values.groupby(pd.Grouper(freq='D')).last().fillna(method='ffill')  # type: pd.DataFrame
    # daily_ret = daily_net.pct_change()
    # cov_matrix = daily_ret.cov()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=std, y=mean, mode='markers'))
    fig.add_trace(go.Scatter(x=[max_sharpe_std], y=[max_sharpe_ret], mode='markers', marker={'symbol':'diamond'}))
    fig.add_trace(go.Scatter(x=[min_var_std], y=[min_var_ret], mode='markers', marker={'symbol':'square'}))

    return fig


# trading activity global

# trading calendar, time

# portfolio live update
