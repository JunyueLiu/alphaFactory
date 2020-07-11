import json
import pickle
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from backtesting.backtesting_metric import aggregate_returns, sharpe_ratio, sortino
from backtesting.dash_app import entry_exit_analysis
from backtesting.dash_app import monthly_analysis
from backtesting.dash_app import trading_history
from backtesting.dash_app import dash_report

from backtesting.dash_app.app import app
from backtesting.plotting import aggregate_returns_heatmap, returns_distribution_plot, entry_and_exit_plot

backtesting_result = None


def get_backtesting_report_dash_app(backtesting_result: dict):
    app.layout = html.Div([
        html.H2('Backtesting Result'),
        dcc.Location(id='url', refresh=False),
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

    index_page = html.Div([
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

        [Input('my-date-picker-range', 'start_date'),
         Input('my-date-picker-range', 'end_date'),
         Input('asset-selection', 'value'),
         Input('timeframe', 'value'),
         Input('ohlc-line', 'value'),
         Input('entrust', 'value'),
         Input('trade_table', 'selected_rows'),
         Input('submit', 'n_clicks')])
    def update_entry_exit(start_date, end_date, symbol, timeframe, line, entrust, selected_rows, n_clicks):
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

        return entry_and_exit_plot(data, trade_graph, symbol, ohlc_graph, entrust=e), \
               trade.to_dict('records'), selected_cond

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
