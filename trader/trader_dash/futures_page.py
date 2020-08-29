from gateway.futu_quote import *
import json
from datetime import timedelta

import dash_core_components as dcc
import dash_html_components as html
import dash_table


def get_layout(futu_quote: FutuQuote):
    layout = html.Div([
        html.Figure(id='futures-bookmap-chart'),
        html.Figure(id='futures-min-chart'),




    ])




    pass