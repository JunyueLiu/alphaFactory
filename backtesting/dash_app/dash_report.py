import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from alpha_research.plotting import pd_to_dash_table
from backtesting.dash_app.app import app
from backtesting.plotting import *


def get_layout(backtesting_result: dict):
    strategy_net_value = backtesting_result['net_value']
    returns = backtesting_result['rate of return']
    net_value = net_value_plot(strategy_net_value)
    ret_dist = returns_distribution_plot(returns)
    under_water = maximum_drawdown_plot(backtesting_result['drawdown_percent'])
    key_performance = {
        'Start capital': "{:.2f}".format(strategy_net_value[0]),
        'End capital': "{:.2f}".format(strategy_net_value[-1]),


        'First traded': backtesting_result['first_traded'],
        'Last traded': backtesting_result['last_traded'],


        'Num of trade': backtesting_result['num_trade'],
        'Win rate %': "{:.2f} %".format(100 * backtesting_result['win_rate']),  # type: float
        'Avg win': "{:.2f}".format(backtesting_result['avg_win']),
        'Avg loss': "{:.2f}".format(backtesting_result['avg_loss']),
        'Payoff ratio': "{:.2f}".format(backtesting_result['payoff_ratio']),
        'Max drawdown': backtesting_result['drawdown_value'].min(),
        'Max drawdown %': "{:.2f} %".format(100 * backtesting_result['drawdown_percent'].min()),

    }
    performance_ss = pd.Series(key_performance, name='Performance')

    layout = html.Div([
        html.Br(),
        html.Div(id='left', children=[
            # todo log scale datetime selection
            dcc.Graph(id='net-value', figure=net_value),
            dcc.Graph(id='returns', figure=ret_dist),
            # todo drawback picture
            dcc.Graph(id='underwater', figure=under_water)
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
            dcc.Markdown(performance_ss.to_markdown())
            # selection of

            # pd_to_dash_table(performance_df, id='key')
        ],

                 style={
                     # 'width': '800px',
                     # 'margin-left': '18px',
                     'float': 'right'
                 }

                 )
    ])
    return layout
