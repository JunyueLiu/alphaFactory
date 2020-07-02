import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from backtesting.dash_app.index_app import app





layout = html.Div([
    html.H1(children='',
            style={
                'font-weight': '400',
                'margin': '0'
            }, id='title'),






    html.Div(id='left', children=[

        # todo 参考别人那个html，用backtesting/plotting画图

    ],

             style={
                 'width': '620px',
                 'margin-right': '18px',
                 'margin-top': '-1.2rem',
                 'float': 'left'
             }),

    html.Div(id='right', children=[
        # todo 参考别人那个html，画table，可能用markdown比较好吧

    ],

             style={
                 'width': '320px',
                 'float': 'right'
             })

])
