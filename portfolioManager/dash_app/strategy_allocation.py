import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
import json
import dash_table
from dash.dependencies import Input, Output, State

from portfolioManager.dash_app.app import app
from portfolioManager.plotting import efficient_frontier_plot
from portfolioManager.utils import calculate_max_sharp_weights


def get_layout(net_values):
    daily_net = net_values.groupby(pd.Grouper(freq='D')).last().fillna(method='ffill')  # type: pd.DataFrame
    daily_ret = daily_net.pct_change()
    annualized_ret_mean = 252 * daily_ret.mean()
    annualized_ret_std = np.sqrt(252) * daily_ret.std()
    annualized_ret_cov = 252 * daily_ret.cov()
    allocations = calculate_max_sharp_weights(annualized_ret_mean, annualized_ret_cov)
    allocations_dict = allocations.to_dict()
    # ef = efficient_frontier_plot(annualized_ret_mean, annualized_ret_std)

    weights = []
    for col in net_values.columns:
        weights.append(html.Div(col + ' Weight (%)', style={'display': 'inline-block'}))
        weights.append(
            dcc.Input(id=col, type='number', value='{:.2f}'.format(100 * allocations_dict['allocation'][col])))

    children = [
        html.Div('annualized factor'),
        dcc.Input(id='annualized-factor', value=252, type='number'),
        html.Button(id='update', children='update'),
        html.Div(weights, id='weights', style={'display': 'block'}),
        dcc.Graph(id='efficient-frontier'),
        dcc.Graph(id='portfolio-netvalue'),
        html.Div(children=net_values.to_json(), id='hidden-netvalue', style={'display': 'none'}),
        html.Div(children=daily_ret.to_json(), id='hidden-ret', style={'display': 'none'}),
        html.Div(children=daily_ret.to_json(), id='hidden-cov', style={'display': 'none'}),
        html.Div(children=allocations.to_json(), id='hidden-weights', style={'display': 'none'})

    ]

    # children.append()

    layout = html.Div(children)
    return layout
