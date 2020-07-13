import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State

from alpha_research.plotting import pd_to_dash_table
from backtesting.dash_app.app import app
from backtesting.plotting import *


def get_layout(backtesting_result: dict):
    has_benchmark = False
    strategy_net_value = backtesting_result['net_value']
    if 'benchmark' in backtesting_result.keys() and backtesting_result['benchmark'] is not None:
        has_benchmark = True
        net_value = net_value_plot(strategy_net_value, benchmark=backtesting_result['benchmark'])
    else:
        net_value = net_value_plot(strategy_net_value)


    returns = backtesting_result['rate of return']

    ret_dist = returns_distribution_plot(returns)
    under_water = maximum_drawdown_plot(backtesting_result['drawdown_percent'])


    draw_down_performance = {
        'Avg Drawdown': "{:.2f}".format(backtesting_result['drawdown_value'].mean()),
        'Avg. Drawdown %': "{:.2f} %".format(100 * backtesting_result['drawdown_percent'].mean()),
        'Max Drawdown': backtesting_result['drawdown_value'].min(),
        'Max Drawdown %': "{:.2f} %".format(100 * backtesting_result['drawdown_percent'].min()),
        # 'Recovery Factor': None,
        'Avg. Drawdown Days': "{:.2f}".format(backtesting_result['drawdown_detail']['days'].mean()),
        'Max. Drawdown Days': "{:.2f}".format(backtesting_result['drawdown_detail']['days'].max()),
        'Calmar': None,
    }







    benchmark_ss = None
    if has_benchmark:
        benchmark_performance = {
            'Benchmark Vol': None,
            'Beta': None,
            'Alpha': None,
            'Cum Abnormal Return': None

        }
        benchmark_ss = pd.Series(benchmark_performance, name='benchmark')


    drawdown_ss = pd.Series(draw_down_performance, name='Drawdown')

    left_children = [
            # todo log scale datetime selection
            dcc.Graph(id='net-value', figure=net_value),
            dcc.Graph(id='returns', figure=ret_dist),
            # todo drawback picture
            dcc.Graph(id='underwater', figure=under_water),
            # todo 参考别人那个html，用backtesting/plotting画图

        ]
    if has_benchmark:
        left_children.append(dcc.Graph(id='benchmark-graph'))
    left_children.append(dcc.Graph(id='top-max-drawdown'))

    right_children = [
        # todo 参考别人那个html，画table，可能用markdown比较好吧
        # todo table troublesome again
        html.Div(children='Risk free rate %'),
        dcc.Input(id='risk-free-rate',
                  value='0', type='number'),
        html.Div(children='Annuliazed factor'),
        dcc.Input(id='annul-factor',
                  value='252', type='number'),
        dcc.Markdown(id='general_markdown'),
        dcc.Markdown(drawdown_ss.to_markdown()),
        # selection of

        # pd_to_dash_table(performance_df, id='key')
    ]
    if has_benchmark:
        right_children.append(dcc.Markdown(benchmark_ss.to_markdown()))
    right_children.append(html.Div('Top k drawdown'))
    right_children.append(
        dcc.Dropdown(id='top-k-drawdown',
                     options=[{'label': i, 'value': i} for i in [1, 3,5, 10]],
                     value=3, clearable=False))
    right_children.append(dcc.Markdown(id='top-k-markdown'))



    layout = html.Div([
        html.Div(id='left', children=left_children,
                 style={
                     'width': '800px',
                     'margin-right': '18px',
                     'float': 'left'
                 }),

        html.Div(id='right', children=right_children,

                 style={
                     'width': '500px',
                     # 'margin-right': '18px',
                     'float': 'right'
                 }

                 )
    ])
    return layout
