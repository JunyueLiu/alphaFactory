import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from backtesting.dash_app.app import app
from datetime import datetime as dt
import dash_table
import re

def get_layout(backtesting_result: dict):
    df = backtesting_result['trade_list']
    orderTime = df['order_time'].tolist()
    orderTime.sort()
    start = orderTime[0].to_pydatetime()
    end = orderTime[-1].to_pydatetime()
    layout = html.Div([
        ### history
        html.H1("History"),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=start,
            max_date_allowed=end,
            initial_visible_month=start,
            end_date=end.date()
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

