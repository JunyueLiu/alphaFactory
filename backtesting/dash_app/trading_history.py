import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from backtesting.dash_app.app import app
from datetime import datetime as dt
import dash_table
import re

def get_layout(backtesting_result: dict):
    df = backtesting_result['trade_list']
    print("entering...")
    layout = html.Div([
        ### history
        html.H1("History"),
        dcc.DatePickerSingle(
            id='date-picker-from',
            min_date_allowed=dt(2019, 7, 2),
            max_date_allowed=dt(2020, 4, 29),
            initial_visible_month=dt(2019, 7, 2),
            date=str(dt(2019, 7, 2, 10, 59, 0))
        ),
        dcc.DatePickerSingle(
            id='date-picker-to',
            min_date_allowed=dt(2019, 7, 2),
            max_date_allowed=dt(2020, 4, 29),
            initial_visible_month=dt(2019, 7, 2),
            date=str(dt(2019, 7, 2, 10, 59, 0))
        ),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            style_cell={'textAlign': 'center'},
            filter_action="native",
            data=df.to_dict('records'),
            style_data_conditional=[
                {
                    'if':{
                        'filter_query': '{order_direction} contains "LONG"',
                    },
                    'backgroundColor': '#d9ffcc'
                },
                {
                    'if': {
                        'filter_query': '{order_direction} contains "SHORT"',
                    },
                    'backgroundColor': '#ffcccc'
                }
            ]
        )
    ])
    return layout

