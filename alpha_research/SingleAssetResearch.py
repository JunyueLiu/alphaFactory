import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from alpha_research import AlphaResearch
from alpha_research.factor_transformation import percentile_factor
from alpha_research.performance_metrics import *
from alpha_research.plotting import *
from alpha_research.plotting import monthly_ic_heatmap_plot
from alpha_research.utils import *
from alpha_research.factor_zoo.alpha_101 import *
from IPython.display import display

import plotly.io as pio

pio.renderers.default = "browser"


class SingleAssetResearch(AlphaResearch):
    # data是传进去的
    def __init__(self, data: pd.DataFrame, out_of_sample: pd.DataFrame = None, split_ratio: float = 0.3,
                 factor_parameters=None):
        super().__init__()

        if out_of_sample is None:
            insample = int(len(data) * split_ratio)
            self.in_sample = data[:insample]
            self.out_of_sample = data[insample:]
        else:
            if list(data.colums) != list(out_of_sample.columns):
                raise AttributeError('The in the sample data and the out of sample data should have same columns')
            self.in_sample = data
            self.out_of_sample = out_of_sample

        self.factor_parameter = factor_parameters
        self.factor = None
        self.out_of_sample_factor = None
        self.factor_timeframe = infer_factor_time_frame(self.in_sample.index)
        self.factor_name = 'Time Series Factor'
        self.factor_percentile_entry = 0.8
        self.alpha_func = None
        self.alpha_func_paras = None

    def set_factor_percentile_entry(self, percentile):
        self.factor_percentile_entry = percentile

    def set_factor_name(self, factor_name):
        self.factor_name = factor_name

    def calculate_factor(self, func, **kwargs):
        self.alpha_func = func
        self.alpha_func_paras = kwargs
        if kwargs is not None:
            factor = func(self.in_sample, **kwargs)
            if isinstance(factor, pd.Series):
                self.factor = factor
            else:
                self.factor = pd.Series(factor, index=self.in_sample.index)
        else:
            factor = func(self.in_sample)
            if isinstance(factor, pd.Series):
                self.factor = factor
            else:
                self.factor = pd.Series(factor, index=self.in_sample.index)

    def evaluate_alpha(self, forward_return_lag: list = None):

        if forward_return_lag is None:
            forward_return_lag = [1, 5, 10]
        returns = calculate_forward_returns(self.in_sample, forward_return_lag)
        # in sample
        # --------- factor summary ---------
        summary = factor_summary(self.factor, self.factor_name)
        pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))
        display(summary)

        # --------- ic table ---------
        ic_table = calculate_ts_information_coefficient(self.factor, returns)
        pd.set_option('display.float_format', lambda x: '{:.5f}'.format(x))
        display(pd.DataFrame(ic_table, columns=[self.factor_name]))

        # --------- factor beta table ---------
        pd.set_option('display.float_format', None)
        ols_table = factor_ols_regression(self.factor, returns)
        display(ols_table)

        # ---------  factor distribution plot ---------
        fig = factor_distribution_plot(self.factor)
        fig.show()
        fig = qq_plot(self.factor)
        fig.show()

        # ---------  ic heatmap ---------
        ic_heatmap = get_monthly_ic(returns, self.factor, forward_return_lag)
        fig = monthly_ic_heatmap_plot(ic_heatmap)
        fig.show()

        # todo factor value verus forward return bubble
        # fig = bubble_chart(self.factor, )

        # --------- factor backtesting ---------
        fig = price_factor_plot(self.in_sample, self.factor)
        fig.show()
        factor_returns = calculate_ts_factor_returns(self.in_sample, self.factor, forward_return_lag)
        fig = returns_plot(factor_returns, self.factor_name)
        fig.show()
        cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
        benchmark = self.in_sample['close'] / self.in_sample['close'][0]
        fig = cumulative_return_plot(cumulative_returns, benchmark=benchmark, factor_name=self.factor_name)
        fig.show()
        # --------- percentile entry and exit ---------
        per_factor = percentile_factor(self.factor, self.factor_percentile_entry)
        fig = entry_and_exit_plot(self.in_sample, per_factor)
        fig.show()

    def out_of_sample_evaluation(self):
        # self.factor是insample的 self.outofsamplefactor是outofsample的

        self.out_of_sample_factor = self.alpha_func(self.out_of_sample, **self.alpha_func_paras)
        # test whether the two time have same distribution
        t_stat, pvalue = in_out_sample_factor_t_test(self.out_of_sample_factor,
                                                     self.factor[-len(self.out_of_sample_factor):])



        # print(t_stat, pvalue)
        fig = overlaid_factor_distribution_plot(self.factor, self.out_of_sample_factor)
        fig.show()
        fig = observed_qq_plot(self.factor, self.out_of_sample_factor)
        fig.show()

    def get_evaluation_dash_app(self):
        """
        :return:
        """
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        # forward_returns_period = [1, 2, 5, 10]  # period list
        # forward_str = str(forward_returns_period).replace('[', '').replace(']', '')

        para_dcc_list = []
        for k, v in self.alpha_func_paras.items():
            para_dcc_list.append(html.Div(children=k))
            para_dcc_list.append(dcc.Input(
                id="input_{}".format(k),
                placeholder=str(k),
                type='number',
                value=str(v), debounce=True
            ))

        app.layout = html.Div(children=[
            html.H1(children=self.factor_name + ' evaluation',
                    style={'font-weight': 'normal', 'text-align': 'center', 'display': 'block',
                           'fontFamily': 'helvetica neue', 'margin': '100px auto'}),

            html.Div([
                # change forward returns
                html.Div([
                    html.Div(id='forward-returns-period'),
                    # add forward returns
                    html.Div(children='Enter a value to add or remove forward return value'),
                    dcc.Input(
                        id='forwards-periods-input',
                        type='text',
                        value='1, 2, 5, 10'
                    ),
                    html.Button('Update', id='UpdateButton'), ]
                    , style={'margin-left': '100px', 'width:': '400px', 'float': 'left'}),
                # change parameter
                html.Div([
                    html.Div(children='Factor Parameter'),
                    html.Div(para_dcc_list, id='alpha_paras'),
                    html.Button('Submit', id='AlphaButton'),
                    html.Div(id="current-parameter"),
                ], style={'margin-left': '400px', 'display': 'inline-block'}),

            ]),

            html.Div([
                dcc.RadioItems(
                    id='in-out-sample',
                    options=[{'label': i, 'value': i} for i in ['In sample', 'Out ot the sample']],
                    value='In sample',
                    labelStyle={'display': 'inline-block'}
                )
            ], style={'display': 'block', 'margin': '0px 100px 50px 100px'}),
            # todo 拯救一下我的表格布局吧，冇眼睇

            # summary table
            html.Div([html.H5(children='Factor Summary Table', style={'width': '49%'}),
                      html.Table(id='summary-table', style={'width': '49%', 'display': 'inline-block'}), ]),

            # ic_table
            html.Div([html.H5(children='Factor IC Table', style={'width': '49%'}),
                      html.Table(id='ic-table',
                                 style={'width': '49%', 'display': 'inline-block'}),
                      ]),

            # beta table
            html.Div([html.H5(children='Factor Beta')
                         , html.Table(id='beta-table', style={'width': '100%', 'display': 'inline-block'})]),

            html.Div([html.H5(children='Factor Distribution', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='distribution')],
                     style={'width': '49%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            html.Div([html.H5(children='Q-Q plot ', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='qqplot')],
                     style={'width': '49%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            html.Div([html.H5(children='Factor IC', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='ic_heatmap')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            html.Div([html.H5(children='Price Factor', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='price_factor')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div([html.H5(children='Factor Return', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='factor-returns')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div([html.H5(children='Factor Backtesting', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='factor-backtest')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div(children=self.factor.to_json(orient='split'), id='in_sample_factor',
                     style={'display': 'none'}),
            html.Div(id='out_sample_factor', style={'display': 'none'}),
            html.Div(children=json.dumps([1, 2, 5, 10]), id='forward_returns_period_saved', style={'display': 'none'}),
            html.Div(id='forward_str', style={'display': 'none'}),
        ], style={'margin': '20px'})

        # make input parameter into dict
        def _get_alpha_parameter_from_div(alpha_paras):
            paras = {}
            for child in alpha_paras:
                if child['type'] == 'Input':
                    props = child['props']
                    k = props['id'].replace('input_', '')
                    v = props['value']
                    try:
                        v = int(v)
                    except:
                        v = float(v)
                    paras[k] = v
            return paras

        @app.callback(Output('in_sample_factor', 'children'),
                      [
                          Input('AlphaButton', 'n_clicks'),
                          Input('alpha_paras', 'children')])
        def update_alpha_insample(n_clicks, alpha_paras):
            # some expensive clean data step
            # print(alpha_paras)
            paras = _get_alpha_parameter_from_div(alpha_paras)
            self.calculate_factor(self.alpha_func, **paras)
            in_sample_factor = self.factor  # type: pd.Series
            # more generally, this line would be
            # json.dumps(cleaned_df)
            return in_sample_factor.to_json(orient='split')

        @app.callback(Output('out_sample_factor', 'children'),
                      [
                          Input('AlphaButton', 'n_clicks'),
                          Input('alpha_paras', 'children')])
        def update_alpha_out_of_sample(n_clicks, alpha_paras):

            paras = _get_alpha_parameter_from_div(alpha_paras)
            self.calculate_factor(self.alpha_func, **paras)

            out_of_sample_factor = self.alpha_func(self.out_of_sample, **paras)  # type: pd.Series

            # more generally, this line would be
            # json.dumps(cleaned_df)
            return out_of_sample_factor.to_json(orient='split')

        @app.callback([Output('forward_returns_period_saved', 'children'),
                       Output("forward-returns-period", "children")],
                      [Input("UpdateButton", "n_clicks")],
                      [State("forwards-periods-input", "value")])
        def update_forward_return(n_clicks, value):
            fr = list(set([int(p) for p in value.split(',')]))
            fr.sort()
            forward_str = str(fr).replace('[', '').replace(']', '')
            return json.dumps(fr), 'Forward return list: ' + forward_str

        @app.callback([
            Output('distribution', 'figure'),
            Output('ic_heatmap', 'figure'),
            Output('qqplot', 'figure'),
            Output('price_factor', 'figure'),
            Output('factor-returns', 'figure'),
            Output('factor-backtest', 'figure'),
            Output('summary-table', 'children'),
            Output('ic-table', 'children'),
            Output('beta-table', 'children'),
        ], [Input("UpdateButton", "n_clicks"),
            Input('in-out-sample', 'value'),
            Input('forward_returns_period_saved', 'children'),
            Input('in_sample_factor', 'children'), Input('out_sample_factor', 'children'), ])
        def update_forward_returns(n_clicks, value, forward_period, alpha_json, out_alpha_json):
            forward_returns_period = json.loads(forward_period)

            factor = pd.read_json(alpha_json, orient='split', typ='series')
            if value == 'In sample':
                update_distribution_figure = factor_distribution_plot(factor)

                returns = calculate_forward_returns(self.in_sample, forward_returns_period)
                ic_heatmap = get_monthly_ic(returns, factor, forward_returns_period)
                update_heatmap_figure = monthly_ic_heatmap_plot(ic_heatmap)

                update_qqplot_figure = qq_plot(factor)

                update_factor_plot_figure = price_factor_plot(self.in_sample, factor)

                factor_returns = calculate_ts_factor_returns(self.in_sample, factor, forward_returns_period)
                update_factor_plot_figure1 = returns_plot(factor_returns, self.factor_name)

                factor_returns = calculate_ts_factor_returns(self.in_sample, factor, forward_returns_period)
                cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
                benchmark = self.in_sample['close'] / self.in_sample['close'][0]
                update_factor_plot_figure2 = cumulative_return_plot(cumulative_returns, benchmark=benchmark,
                                                                    factor_name=self.factor_name)
                # tables
                factor_table = pd_to_dash_table(factor_summary(factor), 'summary')
                ic_table = pd_to_dash_table(pd.DataFrame(calculate_ts_information_coefficient(factor, returns),
                                                         columns=[self.factor_name]), 'ic')
                ols_table = pd_to_dash_table(factor_ols_regression(factor, returns), 'ols')

                return update_distribution_figure, update_heatmap_figure, \
                       update_qqplot_figure, update_factor_plot_figure, \
                       update_factor_plot_figure1, update_factor_plot_figure2, \
                       factor_table, ic_table, ols_table
            else:
                # out of sample的情况还没搞好
                out_factor = pd.read_json(out_alpha_json, orient='split', typ='series')
                # update_distribution_figure = factor_distribution_plot(out_factor)

                returns = calculate_forward_returns(self.out_of_sample, forward_returns_period)

                ic_heatmap = get_monthly_ic(returns, out_factor, forward_returns_period)
                update_heatmap_figure = monthly_ic_heatmap_plot(ic_heatmap)

                # update_qqplot_figure = qq_plot(out_factor)

                update_factor_plot_figure = price_factor_plot(self.out_of_sample, out_factor)

                factor_returns = calculate_ts_factor_returns(self.out_of_sample, out_factor, forward_returns_period)
                update_factor_plot_figure1 = returns_plot(factor_returns, self.factor_name)

                factor_returns = calculate_ts_factor_returns(self.out_of_sample, out_factor, forward_returns_period)
                cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
                benchmark = self.out_of_sample['close'] / self.out_of_sample['close'][0]
                update_factor_plot_figure2 = cumulative_return_plot(cumulative_returns, benchmark=benchmark,
                                                                    factor_name=self.factor_name)
                # for out of sample data onlye
                in_out_distplot = overlaid_factor_distribution_plot(factor, out_factor)
                inout_qqplot = observed_qq_plot(factor, out_factor)
                # inout_qqplot.show()

                factor_table = pd_to_dash_table(factor_summary(out_factor))
                ic_table = pd_to_dash_table(pd.DataFrame(calculate_ts_information_coefficient(out_factor, returns),
                                                         columns=[self.factor_name]))
                ols_table = pd_to_dash_table(factor_ols_regression(out_factor, returns))


                return in_out_distplot, update_heatmap_figure, \
                       inout_qqplot, update_factor_plot_figure, \
                       update_factor_plot_figure1, update_factor_plot_figure2,\
                       factor_table, ic_table, ols_table

        return app


class DemoSingleAssetFactor(SingleAssetResearch):
    def __init__(self, data: pd.DataFrame, out_of_sample: pd.DataFrame = None, split_ratio: float = 0.3,
                 factor_parameters=None):
        super(DemoSingleAssetFactor, self).__init__(data, out_of_sample, split_ratio, factor_parameters)


if __name__ == '__main__':
    data_path = r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'

    df = pd.read_csv(data_path)
    df['time_key'] = pd.to_datetime(df['time_key'])
    df.set_index('time_key', inplace=True)
    df = df[-5000:]
    parameter = {'short_period': 5, 'long_period': 10}

    factor_study = SingleAssetResearch(df)

    # def ma5_ma10(df, time_lag_1 = 5, time_lag2= 10):
    #     pass
    #
    factor_study.calculate_factor(alpha_6, **{'time_lag': 5})
    # factor_study.evaluate_alpha()
    # factor_study.out_of_sample_evaluation()
    factor_study.get_evaluation_dash_app().run_server(debug=True)
    # json = factor_study.factor.to_json(date_format='iso', orient='split')
    # df = pd.read_json(json, orient='split', typ='series')
