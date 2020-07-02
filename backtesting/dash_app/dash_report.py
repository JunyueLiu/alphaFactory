import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from alpha_research.plotting import pd_to_dash_table
from backtesting.dash_app.app import app
from backtesting.plotting import *


def get_layout(backtesting_result: dict):
    strategy_net_value = backtesting_result['net_value']
    returns = backtesting_result['rate of return']
    net_value = net_value_plot(strategy_net_value)
    ret_dist = returns_distribution_plot(returns)

    key_performance = {
        'first_traded': backtesting_result['first_traded'],
        'last_traded': backtesting_result['last_traded'],
        'num_trade': backtesting_result['num_trade'],
        'win_rate': backtesting_result['win_rate'],
        'avg_win': backtesting_result['avg_win'],
        'avg_loss': backtesting_result['avg_loss'],
        'payoff_ratio': backtesting_result['payoff_ratio'],

    }
    performance_df = pd.DataFrame([key_performance])
    print(performance_df)



    layout = html.Div([
        html.Br(),
        html.Div(id='left', children=[
            dcc.Graph(id='net-value', figure=net_value),
            dcc.Graph(id='returns', figure=ret_dist)

            # todo 参考别人那个html，用backtesting/plotting画图

        ],
                 style={
                     'width': '800px',
                     'margin-right': '18px',
                     'margin-top': '-1.2rem',
                     'float': 'left'
                 }),

        html.Div(id='right', children=[
            # todo 参考别人那个html，画table，可能用markdown比较好吧
            # todo table troublesome again
            html.Table(children=pd_to_dash_table(performance_df, id='key'))
            # pd_to_dash_table(performance_df, id='key')
        ],

                 style={
                     'width': '320px',
                     'float': 'right'
                 })

    ])
    return layout
