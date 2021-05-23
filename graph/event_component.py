from plotly import graph_objects as go
import pandas as pd
import plotly.figure_factory as ff


def ret_distribution_component(pnl: pd.Series, label: str, color) -> list:
    """

    :param pnl:
    :param label:
    :param color:
    :return:
    """
    fig = ff.create_distplot([pnl.dropna(), ], [label], bin_size=0.001,
                             colors=[color]
                             )

    fig.add_vline(x=0, line_width=3, line_dash="dash", line_color="red")
    mean = pnl.mean()
    std = pnl.std()
    fig.add_vline(x=mean, line_width=5, line_dash="dash", line_color=color)
    fig.add_vline(x=mean + 2 * std, line_width=5, line_dash="dash", line_color=color)
    fig.add_vline(x=mean - 2 * std, line_width=5, line_dash="dash", line_color=color)
    # hist, fitted_curve, rug, zero = fig.data

    return fig.data


def before_after_ret_dist_component(before_pnl: pd.Series, after_pnl: pd.Series, label: str, ):
    """

    :param before_pnl:
    :param after_pnl:
    :param label:
    :return:
    """
    fig = ff.create_distplot([before_pnl.dropna(), after_pnl.dropna()], ['before_' + label, 'after_' + label], bin_size=0.001,
                             # colors=[color]
                             )


    fig.add_vline(x=0, line_width=3, line_dash="dash", line_color="red")
    return fig.data

def event_chart(series: pd.Series, event_index: int or pd.Timestamp, line_color, line_size):

    return go.Scatter()
    pass

def event_group_chart():
    pass

