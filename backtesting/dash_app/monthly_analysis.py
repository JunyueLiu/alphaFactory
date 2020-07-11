import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from backtesting.dash_app.app import app

def get_layout(backtesting_result: dict):


    layout = html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Daily', 'value': 'D'},
                {'label': 'Week', 'value': 'W'},
                {'label': 'Month', 'value': 'M'},
                {'label': 'Quarter', 'value': 'Q'},
                {'label': 'Year', 'value': 'Y'},
            ],
            value='D',
            clearable=False,
            placeholder="Select a Period",
        ),
        html.Div(id='title'),
        # todo 选择dropdown改日，周，月分析
        html.Div(id='left', children=[
            dcc.Graph(id='return-heatmap'),
            dcc.Graph(id='returns-distribution'),


        ],
                 style={
                     'width': '800px',
                     'margin-right': '18px',
                     # 'margin-top': '-1.2rem',
                     'float': 'left'
                 }),
        # dcc.Graph('')
        html.Div(id='right', children=[
            dcc.Markdown(id='key_period')
            # number of trade?
            # best month
            # worst
            # avg
            #
            # dcc.Markdown(),
            # dcc.Markdown(),
        ],

                 style={
                     'width': '500px',
                     # 'margin-right': '18px',
                     'float': 'right'
                 }

                 )
    ])
    return layout

# @app.callback(Output('title', 'children'), [Input('dropdown', 'value')])
# def change_selection(value):
#     print(value)
#     if value == 'D':
#         return 'Daily Analysis'
#     elif value == 'W':
#         return 'Weekly Analysis'
#     elif value == 'M':
#         return 'Monthly Analysis'