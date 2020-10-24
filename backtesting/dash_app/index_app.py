import json
import pickle
import dash_table
import inspect
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from backtesting.backtesting_metric import aggregate_returns, sharpe_ratio, sortino
from backtesting.dash_app import entry_exit_analysis
from backtesting.dash_app import monthly_analysis
from backtesting.dash_app import trading_history
from backtesting.dash_app import dash_report

from backtesting.dash_app.app import app as app_
from backtesting.plotting import aggregate_returns_heatmap, returns_distribution_plot, entry_and_exit_plot, \
    net_value_plot

from technical_analysis import momentum, statistic_function
from technical_analysis import pattern
from technical_analysis import volume
from technical_analysis import volatility
from technical_analysis import overlap
from technical_analysis import customization

from technical_analysis.momentum import *
from technical_analysis.pattern import *
from technical_analysis.volume import *
from technical_analysis.volatility import *
from technical_analysis.overlap import *
from technical_analysis.customization import *
from technical_analysis.statistic_function import *
from technical_analysis.utils import *


def get_backtesting_report_dash_app(backtesting_result: dict, dash_app=None):
    # global app
    if dash_app is not None:
        app = dash_app
    else:
        app = app_
    app.layout = html.Div([
        html.H2('Backtesting Result'),
        dcc.Location(id='url', refresh=False),
        dcc.Link('Index', href='/'),
        html.Br(),
        dcc.Link('General Performance', href='/btPerformance'),
        # dcc.Tab(),
        html.Br(),
        dcc.Link('Monthly Analysis', href='/monthlyAnalysis'),
        html.Br(),
        # todo holding position question
        dcc.Link('Entry and exit Detail', href='/details'),
        html.Br(),
        dcc.Link('Trading history', href='/history'),
        html.Br(),
        # dcc.Tabs(id='tabs', value='tab', children=[
        #     dcc.Tab(label='General Performance', value='tab-1'),
        #     dcc.Tab(label='Monthly Analysis', value='tab-2'),
        #     dcc.Tab(label='Entry and exit Detail', value='tab-3'),
        #     dcc.Tab(label='Trading history', value='tab-4'),
        #     # dcc.Tab(label='Tab two', value='tab-2'),
        # ]),

        html.Div(id='page-content'),
    ], style={'margin': '30px'})

    profile = json.dumps(backtesting_result['strategy_profile'], indent=2)

    index_page = html.Div([
        html.Pre(profile),
        # todo 行情profile
        # benchmark
        # each stock
        # each time frame
        # strategy basic information
        # name

        # todo 回测类型
        #
    ]),

    # --------------- index page callback ---------------
    @app.callback(Output('page-content', 'children'),
                  [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/btPerformance':
            return dash_report.get_layout(backtesting_result)
        elif pathname == '/monthlyAnalysis':
            return monthly_analysis.get_layout(backtesting_result)
        elif pathname == '/details':
            return entry_exit_analysis.get_layout(backtesting_result)
        elif pathname == '/history':
            return trading_history.get_layout(backtesting_result)
        else:
            return index_page

    # --------------- general page callback ---------------
    @app.callback([Output('general_markdown', 'children')],
                  [Input('risk-free-rate', 'value'),
                   Input('annul-factor', 'value')])
    def update_general_performance(risk_free_rate, annulizaed_factor):
        strategy_net_value = backtesting_result['net_value']
        returns = backtesting_result['rate of return']
        risk_free_rate = float(risk_free_rate)
        annulizaed_factor = int(annulizaed_factor)
        general_performance = {
            'Initial capital': "{:.2f}".format(strategy_net_value[0]),
            'End capital': "{:.2f}".format(strategy_net_value[-1]),

            'Cumulative Return %': "{:.2f} %".format(100 * backtesting_result['cumulative_return']),
            'CAGR %': "{:.2f} %".format(100 * backtesting_result['cagr']),

            'First traded': backtesting_result['first_traded'],
            'Last traded': backtesting_result['last_traded'],

            'Num of trade': backtesting_result['num_trade'],
            'Win rate %': "{:.2f} %".format(100 * backtesting_result['win_rate']),  # type: float
            'Avg win': "{:.2f}".format(backtesting_result['avg_win']),
            'Avg loss': "{:.2f}".format(backtesting_result['avg_loss']),
            'Payoff ratio': "{:.2f}".format(backtesting_result['payoff_ratio']),

            # returns statistics
            'Volatility %': "{:.2f} %".format(100 * backtesting_result['volatility']),
            'Skew': "{:.2f}".format(backtesting_result['skew']),
            'Kurtosis': "{:.2f}".format(backtesting_result['Kurtosis']),
            'Sharpe': "{:.2f}".format(sharpe_ratio(returns, risk_free_rate, annulizaed_factor)),
            'Sortino': "{:.2f}".format(sortino(returns, risk_free_rate, annulizaed_factor)),

        }
        general_ss = pd.Series(general_performance, name='Performance')
        return general_ss.to_markdown(),

    @app.callback([Output('top-k-markdown', 'children'),
                   Output('top-max-drawdown', 'figure')],
                  [Input('top-k-drawdown', 'value')])
    def update_top_drawdown(top_k):
        top_k = int(top_k)
        strategy_net_value = backtesting_result['net_value']
        table = backtesting_result['drawdown_detail'].sort_values(by='max drawdown')[
                :min(top_k, len(backtesting_result['drawdown_detail']))]  # type: pd.DataFrame
        table['max drawdown'] = table['max drawdown'].apply(lambda x: "{:.2f} %".format(100 * x))

        # table['99% max drawdown'] = table['99% max drawdown'].apply(lambda x: "{:.2f} %".format(100 *x))
        table.reset_index(inplace=True)
        table.drop(columns=['99% max drawdown', 'index'], inplace=True)
        fig = net_value_plot(strategy_net_value)

        red_color = ['#CE0000', '#EA0000', '#FF0000',
                     '#FF2D2D', '#FF2D2D', '#FF5151',
                     '#FF7575', '#FF9797', '#FFB5B5',
                     '#FFD2D2']
        shapes = [
            dict(
                type="rect",
                # x-reference is assigned to the x-values
                xref="x",
                # y-reference is assigned to the plot paper [0,1]
                yref="paper",
                x0=row['start'].replace('-', '/'),
                y0=0,
                x1=row['end'].replace('-', '/'),
                y1=1,
                fillcolor=red_color[idx],
                opacity=0.5,
                layer="below",
                line_width=0,
            ) for idx, row in table.iterrows()
        ]
        fig.update_layout(
            shapes=shapes
        )
        return table.to_markdown(), fig

    # --------------- monthly page callback ---------------
    @app.callback([Output('title', 'children'),
                   Output('return-heatmap', 'figure'),
                   Output('returns-distribution', 'figure'),
                   Output('key_period', 'children')
                   ], [Input('dropdown', 'value')])
    def change_selection(value):
        if value == 'D':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'day')  # type: pd.Series
            # todo trade statistics
            # trade_group = backtesting_result['trade_list'].groupby('order_time')

            heatmap = aggregate_returns_heatmap(agg_ret, 'day')
            displot = returns_distribution_plot(agg_ret)
            consec_win = agg_ret.groupby((agg_ret > 0).cumsum())
            consec_loss = agg_ret.groupby((agg_ret < 0).cumsum())
            period_performance = {
                'Best Day': agg_ret.index[agg_ret.argmax()].date(),
                'Best Day Return': "{:.2f} %".format(100 * agg_ret.max()),
                'Worst Day': agg_ret.index[agg_ret.argmin()].date(),
                'Worst Day Return': "{:.2f} %".format(100 * agg_ret.min()),
                'Days of Consecutive Win': consec_win.cumcount().max(),
                'Days of Consecutive Losses': consec_loss.cumcount().max(),
                'Avg Daily Return %': "{:.2f} %".format(100 * agg_ret.mean()),
                'Daily Return Vol %': "{:.2f} %".format(100 * agg_ret.std()),
                'Daily Return Skew': "{:.2f} ".format(agg_ret.skew()),
                'Daily Return Kurt': "{:.2f} ".format(agg_ret.kurt()),
            }

            return 'Daily Analysis', heatmap, displot, pd.Series(period_performance,
                                                                 name='Daily Key Performance').to_markdown()
        elif value == 'W':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'week')
            heatmap = aggregate_returns_heatmap(agg_ret, 'week')
            displot = returns_distribution_plot(agg_ret)
            consec_win = agg_ret.groupby((agg_ret > 0).cumsum())
            consec_loss = agg_ret.groupby((agg_ret < 0).cumsum())
            period_performance = {
                'Best Week': agg_ret.index[agg_ret.argmax()].date(),
                'Best Week Return': "{:.2f} %".format(100 * agg_ret.max()),
                'Worst Week': agg_ret.index[agg_ret.argmin()].date(),
                'Worst Week Return': "{:.2f} %".format(100 * agg_ret.min()),
                'Weeks of Consecutive Win': consec_win.cumcount().max(),
                'Weeks of Consecutive Losses': consec_loss.cumcount().max(),
                'Avg Weekly Return %': "{:.2f} %".format(100 * agg_ret.mean()),
                'Weekly Return Vol %': "{:.2f} %".format(100 * agg_ret.std()),
                'Weekly Return Skew': "{:.2f} ".format(agg_ret.skew()),
                'Weekly Return Kurt': "{:.2f} ".format(agg_ret.kurt()),

            }

            return 'Weekly Analysis', heatmap, displot, pd.Series(period_performance,
                                                                  name='Week Key Performance').to_markdown()
        elif value == 'M':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'month')
            heatmap = aggregate_returns_heatmap(agg_ret, 'month')
            displot = returns_distribution_plot(agg_ret)
            consec_win = agg_ret.groupby((agg_ret > 0).cumsum())
            consec_loss = agg_ret.groupby((agg_ret < 0).cumsum())
            period_performance = {
                'Best Month': agg_ret.index[agg_ret.argmax()].date(),
                'Best Month Return': "{:.2f} %".format(100 * agg_ret.max()),
                'Worst Month': agg_ret.index[agg_ret.argmin()].date(),
                'Worst Month Return': "{:.2f} %".format(100 * agg_ret.min()),
                'Months of Consecutive Win': consec_win.cumcount().max(),
                'Months of Consecutive Losses': consec_loss.cumcount().max(),
                'Avg Monthly Return %': "{:.2f} %".format(100 * agg_ret.mean()),
                'Monthly Return Vol %': "{:.2f} %".format(100 * agg_ret.std()),
                'Monthly Return Skew': "{:.2f} ".format(agg_ret.skew()),
                'Monthly Return Kurt': "{:.2f} ".format(agg_ret.kurt()),

            }

            return 'Monthly Analysis', heatmap, displot, pd.Series(period_performance,
                                                                   name='Monthly Key Performance').to_markdown()
        elif value == 'Q':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'quarter')
            heatmap = aggregate_returns_heatmap(agg_ret, 'quarter')
            displot = returns_distribution_plot(agg_ret)
            consec_win = agg_ret.groupby((agg_ret > 0).cumsum())
            consec_loss = agg_ret.groupby((agg_ret < 0).cumsum())
            period_performance = {
                'Best Quarter': agg_ret.index[agg_ret.argmax()].date(),
                'Best Quarter Return': "{:.2f} %".format(100 * agg_ret.max()),
                'Worst Quarter': agg_ret.index[agg_ret.argmin()].date(),
                'Worst Quarter Return': "{:.2f} %".format(100 * agg_ret.min()),
                'Quarters of Consecutive Win': consec_win.cumcount().max(),
                'Quarters of Consecutive Losses': consec_loss.cumcount().max(),
                'Avg Quarterly Return %': "{:.2f} %".format(100 * agg_ret.mean()),
                'Quarterly Return Vol %': "{:.2f} %".format(100 * agg_ret.std()),
                'Quarterly Return Skew': "{:.2f} ".format(agg_ret.skew()),
                'Quarterly Return Kurt': "{:.2f} ".format(agg_ret.kurt()),

            }

            return 'Quarter Analysis', heatmap, displot, pd.Series(period_performance,
                                                                   name='Quarterly Key Performance').to_markdown()
        elif value == 'Y':
            agg_ret = aggregate_returns(backtesting_result['rate of return'], 'year')
            heatmap = aggregate_returns_heatmap(agg_ret, 'year')
            displot = returns_distribution_plot(agg_ret)
            consec_win = agg_ret.groupby((agg_ret > 0).cumsum())
            consec_loss = agg_ret.groupby((agg_ret < 0).cumsum())
            period_performance = {
                'Best Year': agg_ret.index[agg_ret.argmax()].date(),
                'Best Year Return': "{:.2f} %".format(100 * agg_ret.max()),
                'Worst Year': agg_ret.index[agg_ret.argmin()].date(),
                'Worst Year Return': "{:.2f} %".format(100 * agg_ret.min()),
                'Years of Consecutive Win': consec_win.cumcount().max(),
                'Years of Consecutive Losses': consec_loss.cumcount().max(),
                'Avg Yearly Return %': "{:.2f} %".format(100 * agg_ret.mean()),
                'Yearly Return Vol %': "{:.2f} %".format(100 * agg_ret.std()),
                'Yearly Return Skew': "{:.2f} ".format(agg_ret.skew()),
                'Yearly Return Kurt': "{:.2f} ".format(agg_ret.kurt()),

            }
            return 'Year Analysis', heatmap, displot, pd.Series(period_performance,
                                                                name='Yearly Key Performance').to_markdown()

    # --------------- entry exit page callback ---------------
    @app.callback(Output('timeframe', 'options'),
                  [Input('asset-selection', 'value')])
    def change_display(value):
        return [{'label': i, 'value': i} for i in backtesting_result['data'][value].keys()]

    @app.callback(
        [Output('entry-exit', 'figure'),
         Output('trade_table', 'data'),
         Output('trade_table', 'style_data_conditional')],
        [
            Input('submit', 'n_clicks'), Input('trade_table', 'selected_rows')],
        [State('ta-list', 'children'),
         State('my-date-picker-range', 'start_date'),
         State('my-date-picker-range', 'end_date'),
         State('asset-selection', 'value'),
         State('timeframe', 'value'),
         State('ohlc-line', 'value'),
         State('entrust', 'value'),
         ])
    def update_entry_exit(n_clicks, selected_rows, ta_dict, start_date, end_date, symbol, timeframe, line, entrust):
        data = backtesting_result['data'][symbol][timeframe]  # type: pd.DataFrame
        data = data[(data.index >= pd.to_datetime(start_date)) & (data.index <= pd.to_datetime(end_date))]
        trade = backtesting_result['trade_list']
        trade = trade[
            (trade['order_time'] >= pd.to_datetime(start_date)) & (trade['order_time'] <= pd.to_datetime(end_date))]
        ohlc_graph = True
        # print(entrust)
        if len(selected_rows) > 0:
            trade_graph = trade.iloc[selected_rows]
            selected_cond = [{
                'if': {'row_index': i},
                'background_color': '#D2F3FF'
            } for i in selected_rows]

        else:
            trade_graph = trade
            selected_cond = []

        if line == 'line':
            ohlc_graph = False
        e = False
        if entrust is None or len(entrust) == 0:
            e = False
        else:
            e = True
        ta = json.loads(ta_dict)
        return entry_and_exit_plot(data, trade_graph, symbol, ohlc_graph, entrust=e, ta_dict=ta), \
               trade.to_dict('records'), selected_cond

    @app.callback(Output('indicator-name', 'options'),
                  [Input('indicator-category', 'value')])
    def update_ta(category):
        l = []
        if category == 'customization':
            l = customization.__func__
        elif category == 'momentum':
            l = momentum.__func__
        elif category == 'volatility':
            l = volatility.__func__
        elif category == 'overlap':
            l = overlap.__func__
        elif category == 'volume':
            l = volume.__func__
        elif category == 'pattern':
            l = pattern.__func__
        elif category == 'statistic_function':
            l = statistic_function.__func__

        return [{'label': i, 'value': i} for i in l]

    @app.callback(Output('parameter', 'children'),
                  [Input('indicator-name', 'value')])
    def update_ta_parameter(ta_name):
        if ta_name is None:
            return None
        func = eval(str(ta_name))
        para_dict = inspect.signature(func).parameters
        children = []
        for k, v in para_dict.items():
            if k == 'inputs':
                continue
            else:
                # todo can it possible to make it a line?
                children.append(html.H6(k, style={'displace': 'inline-block'}))
                if isinstance(v.default, MA_Type):
                    value = v.default.name
                    children.append(dcc.Dropdown(
                        id=k,
                        options=[
                            {'label': label, 'value': label}
                            for label, value_ in v.default._member_map_.items()
                        ],
                        value=value,

                    ))
                else:
                    value = v.default
                    children.append(dcc.Input(id=k, value=value, debounce=True))
        return children

    @app.callback([Output('ta-list', 'children'),
                   Output('remove-name', 'options')],
                  [
                      Input('add-indicator', 'n_clicks', ),
                      Input('remove-indicator', 'n_clicks')],
                  [State('indicator-name', 'value'),
                   State('parameter', 'children'),
                   State('overlap', 'value'),
                   State('remove-name', 'value'),
                   State('ta-list', 'children')]
                  )
    def update_ta_list(add_clicks, remove_clicks, indicator, parameters, overlap, remove, ta_list):
        if ta_list is None:
            ta_dict = {}
        else:
            ta_dict = json.loads(ta_list)
        if indicator is not None:
            indicator_str = ''
            indicator_str += indicator
            indicator_str += '(inputs, '
            for p in parameters:
                if p['type'] == 'Input':
                    if p['props']['value'] == '' or p['props']['value'] is None:
                        continue
                    indicator_str += p['props']['id']

                    if type(p['props']['value']) == float:
                        value = str(p['props']['value'])
                    elif type(p['props']['value']) == int:
                        value = str(p['props']['value'])
                    elif type(p['props']['value']) == str:
                        if p['props']['value'][0].isdigit():
                            value = p['props']['value']
                    else:
                        value = "'" + p['props']['value'] + "'"
                    indicator_str += "=" + value + ','
                elif p['type'] == 'Dropdown':
                    indicator_str += p['props']['id'] + '=MA_Type.' + p['props']['value'] + ','
            indicator_str += ')'
            ta_dict[indicator_str] = True if 'overlap' in overlap else False
            if remove is not None:
                try:
                    del ta_dict[remove]
                except:
                    remove = None
            options = [{'label': i, 'value': i} for i in ta_dict.keys()]
            return json.dumps(ta_dict), options
        else:
            if remove is not None:
                try:
                    del ta_dict[remove]
                except:
                    remove = None
            options = [{'label': i, 'value': i} for i in ta_dict.keys()]
            return json.dumps(ta_dict), options

    # --------------- trade list page callback ---------------

    @app.callback(
        Output('table', 'data'),
        [Input('date-picker-range', 'start_date'), Input('date-picker-range', 'end_date')])
    def update_output(date_from, date_to):
        if date_to is None or date_from is None:
            return
        df = backtesting_result['trade_list']
        df_ = df[(df['order_time'] >= pd.to_datetime(date_from)) & (df['order_time'] <= pd.to_datetime(date_to))]
        return df_.to_dict('records')

    return app


if __name__ == '__main__':
    # app.run_server(host='127.0.0.1', debug=True)
    with open(r'../backtesting_result_sample.pickle', 'rb') as f:
        backtesting_result = pickle.load(f)
    _app = get_backtesting_report_dash_app(backtesting_result)
    _app.run_server(host='127.0.0.1', debug=True, port=8005)
