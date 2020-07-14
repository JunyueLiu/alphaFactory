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
def ret_heatmap(net_values: pd.DataFrame):
    ret = net_values.pct_change().groupby(pd.Grouper(freq='M')).sum()
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



# overall exposure to some asset
## select day and see pie chart

# trading activity global

# trading calendar, time

# portfolio live update
