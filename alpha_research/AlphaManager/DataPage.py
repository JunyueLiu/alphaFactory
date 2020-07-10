from db_wrapper.mongodb_utils import MongoConnection
import dash

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
import pickle
import json
from IPython.core.display import display

from alpha_research import AlphaResearch
from alpha_research.plotting import *
from alpha_research.utils import *
from alpha_research.performance_metrics import *

import plotly.io as pio

def get_layout(df):

    orderTime = df['time_key'].tolist()
    orderTime.sort()
    layout = html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            style_cell={'textAlign': 'center'},
            filter_action="native",
            data=df.to_dict('records'),
            style_data_conditional=[
                {
                    'if': {
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


def get_evaluation_dash_app():

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout= html.Div([html.H3('Alpha manager'),
    html.Div([

    html.Div(['IP:  ',dcc.Input(id='ip', value='',type='text')],style={

    }),
    html.Div(['PORT:  ', dcc.Input(id='port', value='27017', type='text')]),

    html.Div(['USER:  ', dcc.Input(id='user', value='root', type='text')]),
    html.Div(['PASSWORD:  ', dcc.Input(id='password', value='', type='password')]),

    ], style={
        'width':'600px',
        'columnCount': 2
              }),
                          html.Br(),
    html.Button('connect', id='connect'),
    html.Div(id='output-state'),
         ])

    @app.callback(Output('output-state', 'children'),
                  [Input('connect', 'n_clicks')],
                  [State('ip', 'value'),
                   State('port', 'value'),
                   State('user', 'value'),
                   State('password', 'value')])


    def sign_in_mongo(n_clicks,ip,port,user,password):
        # con = MongoConnection(ip,int(port), user,password)
        #
        # df = con.read_mongo_df('quant', 'hsi_1_min', {}, {'time_key': 1, 'close': 1, 'open': 1,
        #                                                   'high': 1, 'low': 1, 'turnover': 1})

        data = {
            'time_key': [1,2,3,4,5,6],
            'open': [1,2,3,4,5,6],
            'close': [1,2,3,4,5,6]
        }

        df =pd.DataFrame(data)


        return get_layout(df)



    return app


if __name__ == '__main__':
    # # connect mongodb
    # # need times

    # df = con.read_mongo_df('quant', 'hsi_1_min', {}, {'time_key': 1, 'close': 1, 'open': 1,
    #                                                   'high': 1, 'low': 1, 'turnover': 1})
    # print(df)

    get_evaluation_dash_app().run_server(host='127.0.0.1', debug=True)

