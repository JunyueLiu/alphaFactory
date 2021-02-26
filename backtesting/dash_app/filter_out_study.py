import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from backtesting.dash_app.app import app
from datetime import datetime as dt
import dash_table
import re


def get_layout(backtesting_result: dict):
    layout = html.Div([





    ])
    return layout