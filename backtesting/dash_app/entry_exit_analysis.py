import json
from datetime import timedelta

import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from backtesting.dash_app.app import app

import technical_analysis


def get_layout(backtesting_result: dict):
    # todo https://dash.plotly.com/interactive-graphing
    symbol = backtesting_result['trade_list']['code'].unique()
    min_date = backtesting_result['trade_list']['order_time'].min().date()
    max_date = backtesting_result['trade_list']['order_time'].max().date()

    layout = html.Div([

        html.Div([

            html.H6('Date range'),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                initial_visible_month=max_date,
                start_date=max_date - timedelta(days=20),
                end_date=max_date
            ),
            html.H6('Instrument'),
            dcc.Dropdown(
                id='asset-selection',
                options=[{'label': s, 'value': s} for s in symbol],
                value=symbol[0]

            ),
            html.H6('Timeframe'),
            dcc.Dropdown(
                id='timeframe',
                value=list(backtesting_result['data'][symbol[0]].keys())[0]

            ),
            dcc.RadioItems(
                id='ohlc-line',
                options=[{'label': 'Candles', 'value': 'ohlc'},
                         {'label': 'line', 'value': 'line'}],
                value='line'

            ),
            dcc.Checklist(
                id='entrust',
                options=[
                    {'label': 'Show Entrust', 'value': 'Entrust'},

                ],

            ),
            html.Button(
                children='Submit',
                id='submit'
            ),
        ], style={'width': '49%', 'display': 'inline-block'}),
        # graph

        # todo dropdown to add technical indicator
        html.Div([
            html.H6('Technical indicator'),
            html.Div([
                dcc.Dropdown(id='indicator-category',
                             options=[{'label': i, 'value': i}
                                      for i in technical_analysis.__all__],
                             placeholder='select category'),
                dcc.Dropdown(id='indicator-name',
                             # options=[{'label': i, 'value': i}
                             #          for i in overlap.__func__],
                             placeholder='select indicator',

                             ),
            ]),
            html.Div(id='parameter'),

            dcc.Checklist(
                id='overlap',
                options=[
                    {'label': 'overlap', 'value': 'overlap'},

                ], value=['overlap']

            ),
            html.Button('Add', id='add-indicator', n_clicks=0),
            dcc.Dropdown(id='remove-name',
                         # options=[{'label': i, 'value': i}
                         #          for i in overlap.__func__],
                         placeholder='select indicator to remove',
                         ),
            html.Button('Remove', id='remove-indicator'),

        ], style={'width': '49%', 'display': 'inline-block', 'float': 'right', 'overflow': 'auto', 'height': '360px'}),

        html.Div(id='left', children=[
            dcc.Graph(id='entry-exit'),
            # dcc.Graph(id='returns-distribution'),

        ],
                 style={
                     # 'width': '1200px',
                     # 'margin-right': '18px',
                     # 'margin-top': '-1.2rem',
                     # 'float': 'left'
                 }),
        # dcc.Graph('')
        html.Div(id='right', children=[
            dash_table.DataTable(
                id='trade_table',
                columns=[
                    {"name": i, "id": i, "deletable": True, "selectable": True} for i in
                    backtesting_result['trade_list'].columns
                ],
                sort_mode="multi",
                row_selectable="multi",
                selected_rows=[],
            )
            # html.Div(id='hover-data')
        ],

                 style={
                     # 'width': '1200px',
                     # 'margin-right': '18px',
                     # 'float': 'right'
                 }

                 ),
        html.Div(id='ta-list', children=json.dumps(dict()), style={'display': 'none'}),
        # html.Div(id='ta-temp', style={'display': 'none'}),

    ])
    return layout
