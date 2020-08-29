from futu.quote.quote_get_warrant import Request

from gateway.futu_quote import *
from gateway.futu_brokerage import *
import json
from datetime import timedelta

import dash_core_components as dcc
import dash_html_components as html
import dash_table




def get_layout(futu_quote: FutuQuote, futu_brokerage: FutuBrokerage):
    layout = html.Div([
        # bull







    ])