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

pio.renderers.default = "browser"


class MultiAssetResearch(AlphaResearch):
    """


    """

    def __init__(self, data: pd.DataFrame, out_of_sample: pd.DataFrame = None, split_ratio: float = 0.3,
                 factor_parameters=None, benchmark: pd.DataFrame = None):
        """
        data is multi index asset price, with first index is time, second index is symbol
        :param data:
        :param out_of_sample:
        :param split_ratio:
        :param factor_parameters:
        """
        super().__init__()
        if out_of_sample is None:
            insample = int(len(data) * split_ratio)
            self.in_sample = data[:insample]
            self.out_of_sample = data[insample:]
            self.alpha_universe = self.in_sample.index.get_level_values(level=1).drop_duplicates()
        else:
            if list(data.colums) != list(out_of_sample.columns):
                raise AttributeError('The in the sample data and the out of sample data should have same columns')
            self.in_sample = data
            self.out_of_sample = out_of_sample

        self.factor_parameter = factor_parameters
        self.factor = None
        self.merged_data = None
        self.out_of_sample_factor = None
        self.factor_timeframe = infer_factor_time_frame(self.in_sample.index.get_level_values(0))
        self.factor_name = 'Cross Sectional Factor'
        self.factor_quantile_list = None
        self.factor_bin_num = 5
        self.asset_group = None

        self.alpha_func = None
        self.alpha_func_paras = None
        self.alpha_position_func = calculate_position

        if benchmark is not None:
            # todo compare the index in the benchmark and the first level of the index
            # make sure the benchmark contains the date in the first level of the index
            self.benchmark = benchmark
        else:
            self.benchmark = benchmark

    def set_factor_quantile_list(self, quantile_list):
        self.factor_quantile_list = quantile_list
        self.factor_bin_num = None

    def set_from_alpha_to_position_func(self, func):
        # todo check whether this function is valid
        self.alpha_position_func = func

    def set_factor_bin(self, bin_num):
        self.factor_bin_num = bin_num
        self.factor_quantile_list = None

    def set_asset_group(self, group: dict):
        diff = set(self.in_sample.index.get_level_values(level=1)) - set(group.keys())
        if len(diff) > 0:
            raise KeyError(
                "Assets {} not in group mapping".format(
                    list(diff)))
        self.asset_group = group

    def set_benchmark(self, df):
        # todo check benchmark is valid or not
        self.benchmark = df

    def calculate_factor(self, func, **kwargs):
        self.alpha_func = func
        self.alpha_func_paras = kwargs
        if kwargs is not None:
            factor = func(self.in_sample, **kwargs)
            assert type(factor) == pd.Series
            assert np.array_equal(factor.index, self.in_sample.index)
            assert factor.values.shape[0] == self.in_sample.shape[0]
        else:
            factor = func(self.in_sample)  # type:pd.Series
            assert type(factor) == pd.Series
            assert np.array_equal(factor.index, self.in_sample.index)
            assert factor.values.shape[0] == self.in_sample.shape[0]
        factor.name = self.factor_name
        self.factor = factor
        self.merged_data = pd.DataFrame(index=factor.index)
        self.merged_data['factor'] = factor
        if self.asset_group is not None:
            ss = pd.Series(self.asset_group)
            groupby = pd.Series(index=self.factor.index,
                                data=ss[self.factor.index.get_level_values(level=1)].values)
            self.merged_data['group'] = groupby.astype('category')

    def evaluate_alpha(self, forward_return_lag: list = None):
        """

        :param forward_return_lag:
        :return:
        """
        if forward_return_lag is None:
            forward_return_lag = [1, 5, 10]
        returns = calculate_forward_returns(self.in_sample, forward_return_lag)
        merged_data = self.merged_data.join(returns)  # type: pd.DataFrame
        # in sample
        # ---------  factor summary ---------
        summary = factor_summary(self.factor, self.factor_name)
        pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))
        display(summary)

        # --------- ic table ---------

        ic = calculate_cs_information_coefficient(merged_data)
        pd.set_option('display.float_format', lambda x: '{:.5f}'.format(x))
        display(information_analysis(ic))

        # --------- factor beta table ---------
        pd.set_option('display.float_format', None)
        ols_table = factor_ols_regression(self.factor, returns)
        display(ols_table)

        # factor distribution plot
        fig = factor_distribution_plot(self.factor)
        fig.show()
        fig = qq_plot(self.factor)
        fig.show()

        # to calculate factor return and cumulative return, first need to transform the alpha into position of holding
        # position time series of each asset
        position = self.alpha_position_func(self.factor)

        # --------- factor returns ---------
        factor_returns = calculate_cross_section_factor_returns(self.in_sample, position)
        fig = returns_plot(factor_returns, self.factor_name)
        fig.show()

        cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
        fig = cumulative_return_plot(cumulative_returns, benchmark=self.benchmark, factor_name=self.factor_name)
        fig.show()

        # --------- turnover analysis ---------
        turnover = position_turnover(position)
        display(turnover_analysis(turnover))
        # position graph
        fig = position_plot(position)
        fig.show()
        # turnover time series graph
        fig = turnover_plot(turnover)
        fig.show()

        # ---------  Return analysis ---------
        # return by factor bin
        factor_quantile = quantize_factor(merged_data, self.factor_quantile_list,
                                          self.factor_bin_num)  # type: pd.Series
        merged_data['factor_quantile'] = factor_quantile
        quantile_ret_ts, mean_ret, std_error_ret = mean_return_by_quantile(merged_data)
        display(mean_ret)

        # ---------  Quantile analysis ---------
        # returns by quantile bar
        fig = returns_by_quantile_bar_plot(mean_ret)
        fig.show()
        # return by quantile heatmap
        fig = returns_by_quantile_heatmap_plot(mean_ret)
        fig.show()
        # quantile ret distribution
        fig = returns_by_quantile_distplot(quantile_ret_ts)
        fig.show()
        # cumulative return by quantile
        cum_ret_by_qt = calculate_cumulative_returns_by_quantile(quantile_ret_ts)
        fig = cumulative_returns_by_quantile_plot(cum_ret_by_qt['1_period_return'])
        fig.show()
        # todo by user defined group
        # print(factor_quantile)

    def get_evaluation_dash_app(self):
        # demand:
        # change forward return parameter
        # change alpha universe and redo the calculation
        # change quantile or bin number
        # select and look at specific month performance
        # split section by analysis type:

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        # todo should can customized the bin or quantile list in the dash app

        url_bar_and_content_div = html.Div(children=[
            html.H1(children=self.factor_name + ' evaluation',
                    style={'font-weight': 'normal', 'text-align': 'center', 'display': 'block',
                           'fontFamily': 'helvetica neue', 'margin': '100px auto'}),
            # page selection
            html.Div([
                # represents the URL bar, doesn't render anything
                dcc.Location(id='url', refresh=False),
                dcc.Link('General', href='/general'),
                html.Br(),
                dcc.Link('Factor Quantile Analysis', href='/quantileAnalysis'),
                html.Br(),
                dcc.Link('Group Analysis', href='/groupAnalysis'),

                # content will be rendered in this element
                html.Div(id='page-content')
            ]),

        ], style={'margin': '20px'})

        para_dcc_list = []
        for k, v in self.alpha_func_paras.items():
            para_dcc_list.append(html.Div(children=k))
            para_dcc_list.append(dcc.Input(
                id="input_{}".format(k),
                placeholder=str(k),
                type='number',
                value=str(v), debounce=True
            ))

        general_div = html.Div(children=[html.Div([
            # add forward returns
            html.Div([
                html.Div(id='forward-returns-period'),
                html.Div(children='Enter a value to add or remove forward return value'),
                dcc.Input(
                    id='forwards-periods-input',
                    type='text',
                    value='1, 2, 5, 10'
                ),
                dcc.RadioItems(
                    id='in-out-sample',
                    options=[{'label': i, 'value': i} for i in ['In sample', 'Out ot the sample']],
                    value='In sample',
                    labelStyle={'display': 'inline-block'}
                ),
                html.Button('Update', id='UpdateButton'), ]
                , style={'margin-left': '100px', 'width:': '400px', 'float': 'left'}),
            # change parameter
            html.Div([
                html.Div(children='Factor Parameter'),
                html.Div(para_dcc_list, id='alpha_paras'),
                html.Button('Submit', id='AlphaButton'),
                html.Div(id="current-parameter"),
            ], style={'margin-left': '400px', 'display': 'inline-block'})],
            style={'margin-left': '100px', 'width:': '400px', 'float': 'left'}),
            # select of factor universe
            html.Div([html.H5(children='Alpha Universe',
                              style={'text-align': 'center', 'margin': 'auto'}),
                      # todo 位置需要调一下
                      dcc.Checklist(id='alpha-universe',
                                    options=[{'label': i, 'value': i} for i in self.alpha_universe],
                                    value=self.alpha_universe, labelStyle={'display': 'inline-block'},
                                    )], style={'width': '100%', 'display': 'block', }),

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

            html.Div(
                [html.H5(children='Factor Distribution', style={'text-align': 'center', 'margin': 'auto'}),
                 dcc.Graph(id='distribution')],
                style={'width': '49%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            html.Div([html.H5(children='Q-Q plot ', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='qqplot')],
                     style={'width': '49%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            # html.Div([html.H5(children='Factor IC', style={'text-align': 'center', 'margin': 'auto'}),
            #           dcc.Graph(id='ic_heatmap')],
            #          style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            # html.Div([html.H5(children='Price Factor', style={'text-align': 'center', 'margin': 'auto'}),
            #           dcc.Graph(id='price_factor')],
            #          style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div([html.H5(children='Factor Return', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='factor-returns')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div([html.H5(children='Factor Backtesting', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='factor-backtest')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            html.Div([html.H2(children='Turnover Analysis', style={'text-align': 'center', 'margin': 'auto'}),
                      html.H5(children='Positions', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='position-ts')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            html.Div([html.H5(children='Turnover', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='turnover-ts')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            # save data in the front end
            html.Div(children=json.dumps(list(self.factor.index.names)),
                     id='factor_index_name_saved',
                     style={'display': 'none'}),
            html.Div(children=self.factor.reset_index().to_json(), id='in_sample_factor',
                     style={'display': 'none'}),
            html.Div(id='out_sample_factor', style={'display': 'none'}),
            html.Div(children=json.dumps([1, 2, 5, 10]), id='forward_returns_period_saved',
                     style={'display': 'none'}),
            html.Div(id='forward_str', style={'display': 'none'}),
        ])

        quantile_div = html.Div(children=[html.Div([
            # add forward returns
            html.Div([
                html.Div(id='forward-returns-period'),
                html.Div(children='Enter a value to add or remove forward return value'),
                dcc.Input(
                    id='forwards-periods-input_1',
                    type='text',
                    value='1, 2, 5, 10'
                ),
                dcc.RadioItems(
                    id='in-out-sample_1',
                    options=[{'label': i, 'value': i} for i in ['In sample', 'Out ot the sample']],
                    value='In sample',
                    labelStyle={'display': 'inline-block'}
                ),

                html.Div(id='quantile parameter'),
                html.Div(children='Enter a value to change quantile or bin'),
                # todo quantile selection
                dcc.Input(
                    id='quantile',
                    type='text',
                    value='0, 20, 40, 60, 80, 100', debounce=True
                ),
                dcc.Input(
                    id='bin',
                    type='number',
                    value='5',
                    min='1',
                    debounce=True
                ),
                html.Button('Update', id='UpdateButton_1'), ]
                , style={'margin-left': '100px', 'width:': '400px', 'float': 'left'}),
            # change parameter
            html.Div([
                html.Div(children='Factor Parameter'),
                html.Div(para_dcc_list, id='alpha_paras_1'),
                html.Button('Submit', id='AlphaButton_1'),
                html.Div(id="current-parameter_1"),
            ], style={'margin-left': '400px', 'display': 'inline-block'})],
            style={'margin-left': '100px', 'width:': '400px', 'float': 'left'}),
            # select of factor universe
            html.Div([html.H5(children='Alpha Universe',
                              style={'text-align': 'center', 'margin': 'auto'}),
                      # todo 位置需要调一下
                      dcc.Checklist(id='alpha-universe_1',
                                    options=[{'label': i, 'value': i} for i in self.alpha_universe],
                                    value=self.alpha_universe,
                                    labelStyle={'display': 'inline-block'},
                                    )], style={'width': '100%', 'display': 'block', }),

            html.Div([html.H5(children='Returns by Quantile Bar', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='quantile-bar')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div([html.H5(children='Quantile heatmap', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='quantile-heatmap')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),
            html.Div([html.H5(children='Returns by Displot', style={'text-align': 'center', 'margin': 'auto'}),
                      dcc.Graph(id='quantile-displot')],
                     style={'width': '100%', 'display': 'inline-block', 'margin-bottom': '50px'}),

            # todo hidden data
            html.Div(children=json.dumps(list(self.factor.index.names)),
                     id='factor_index_name_saved_1',
                     style={'display': 'none'}),
            html.Div(children=self.factor.reset_index().to_json(), id='in_sample_factor_1',
                     style={'display': 'none'}),
            html.Div(id='out_sample_factor_1', style={'display': 'none'}),
            html.Div(children=json.dumps([1, 2, 5, 10]), id='forward_returns_period_saved_1',
                     style={'display': 'none'}),

        ]

        )

        group_div = html.Div(children=[

        ])

        app.layout = url_bar_and_content_div

        app.validation_layout = html.Div([
            url_bar_and_content_div,
            general_div,
            quantile_div,
            group_div

        ])

        # for switching the pages
        @app.callback(dash.dependencies.Output('page-content', 'children'),
                      [dash.dependencies.Input('url', 'pathname')])
        def display_page(pathname):
            if pathname == '/general':
                return general_div
            elif pathname == '/quantileAnalysis':
                return quantile_div
            elif pathname == '/groupAnalysis':
                return group_div

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

        # for update change of parameter in the general page
        @app.callback(Output('in_sample_factor', 'children'),
                      [
                          Input('AlphaButton', 'n_clicks'),
                          Input('alpha_paras', 'children')])
        def update_alpha_insample(n_clicks, alpha_paras):
            paras = _get_alpha_parameter_from_div(alpha_paras)
            self.calculate_factor(self.alpha_func, **paras)
            in_sample_factor = self.factor  # type: pd.Series
            # more generally, this line would be
            # json.dumps(cleaned_df)
            # print(in_sample_factor)
            # json.dumps(in_sample_factor)
            # todo the multiIndex pd.Series object will break if read_json
            # potential solution:
            # in_sample_factor.reset_index().to_json()
            # todo pickle solution unsuccessful
            return in_sample_factor.reset_index().to_json()

        @app.callback(Output('out_sample_factor', 'children'),
                      [
                          Input('AlphaButton', 'n_clicks'),
                          Input('alpha_paras', 'children')])
        def update_alpha_out_of_sample(n_clicks, alpha_paras):

            paras = _get_alpha_parameter_from_div(alpha_paras)
            self.calculate_factor(self.alpha_func, **paras)

            out_of_sample_factor = self.alpha_func(self.out_of_sample, **paras)  # type: pd.Series
            out_of_sample_factor.name = self.factor_name
            # more generally, this line would be
            # json.dumps(cleaned_df)
            return out_of_sample_factor.reset_index().to_json()

        @app.callback([Output('forward_returns_period_saved', 'children'),
                       Output("forward-returns-period", "children")],
                      [Input("UpdateButton", "n_clicks")],
                      [State("forwards-periods-input", "value")])
        def update_forward_return(n_clicks, value):
            fr = list(set([int(p) for p in value.split(',')]))
            fr.sort()
            forward_str = str(fr).replace('[', '').replace(']', '')
            return json.dumps(fr), 'Forward return list: ' + forward_str

        # todo maybe table could move out to get faster table calculation?
        @app.callback([
            Output('distribution', 'figure'),
            Output('qqplot', 'figure'),
            Output('factor-returns', 'figure'),
            Output('factor-backtest', 'figure'),
            Output('summary-table', 'children'),
            Output('ic-table', 'children'),
            Output('beta-table', 'children'),
            Output('turnover-ts', 'figure'),
            Output('position-ts', 'figure')
        ], [Input("UpdateButton", "n_clicks"),
            Input('in-out-sample', 'value'),
            Input('forward_returns_period_saved', 'children'),
            Input('in_sample_factor', 'children'),
            Input('out_sample_factor', 'children'),
            Input('factor_index_name_saved', 'children'),
            ])
        def update_forward_returns(n_clicks,
                                   value,
                                   forward_period,
                                   in_alpha_json,
                                   out_alpha_json,
                                   factor_index_name_saved
                                   ):
            forward_returns_period = json.loads(forward_period)
            factor_index_ = json.loads(factor_index_name_saved)
            factor = pd.read_json(in_alpha_json)
            factor.set_index(factor_index_, inplace=True)
            # todo factor selection by universe list
            factor = factor[self.factor_name]
            if value == 'In sample':
                # --------- calculation first ---------
                returns = calculate_forward_returns(self.in_sample, forward_returns_period)
                position = self.alpha_position_func(factor)
                merged_data = pd.DataFrame(index=factor.index)
                merged_data['factor'] = factor

                factor_returns = calculate_cross_section_factor_returns(self.in_sample, position)
                cumulative_returns = calculate_cumulative_returns(factor_returns, 1)

                # ------- factor distribution study ---------
                update_distribution_figure = factor_distribution_plot(factor)
                update_qqplot_figure = qq_plot(factor)

                # --------- factor returns ---------
                update_factor_plot_figure1 = returns_plot(factor_returns, self.factor_name)

                update_factor_plot_figure2 = cumulative_return_plot(cumulative_returns, benchmark=self.benchmark,
                                                                    factor_name=self.factor_name)

                # --------- turnover analysis ---------
                turnover = position_turnover(position)
                # display(turnover_analysis(turnover))
                # position graph
                pos_graph = position_plot(position)
                # turnover time series graph
                turnover_ts = turnover_plot(turnover)

                # ic_heatmap = get_monthly_ic(returns, factor, forward_returns_period)
                # update_heatmap_figure = monthly_ic_heatmap_plot(ic_heatmap)

                # -------- tables --------
                factor_table = pd_to_dash_table(factor_summary(factor), 'summary')

                ic = calculate_cs_information_coefficient(merged_data)
                display(information_analysis(ic))

                ic_table = pd_to_dash_table(pd.DataFrame(calculate_ts_information_coefficient(factor, returns),
                                                         columns=[self.factor_name]), 'ic')
                ols_table = pd_to_dash_table(factor_ols_regression(factor, returns), 'ols')

                return update_distribution_figure, update_qqplot_figure, \
                       update_factor_plot_figure1, update_factor_plot_figure2, \
                       factor_table, ic_table, ols_table, turnover_ts, pos_graph
            else:
                out_factor = pd.read_json(out_alpha_json)
                out_factor.set_index(factor_index_, inplace=True)
                out_factor = out_factor[self.factor_name]

                returns = calculate_forward_returns(self.out_of_sample, forward_returns_period)
                position = self.alpha_position_func(out_factor)
                merged_data = pd.DataFrame(index=factor.index)
                merged_data['factor'] = factor

                factor_returns = calculate_cross_section_factor_returns(self.out_of_sample, position)
                cumulative_returns = calculate_cumulative_returns(factor_returns, 1)

                # update_distribution_figure = factor_distribution_plot(out_factor)

                returns = calculate_forward_returns(self.out_of_sample, forward_returns_period)

                # for out of sample data onlye
                in_out_distplot = overlaid_factor_distribution_plot(factor, out_factor)
                inout_qqplot = observed_qq_plot(factor, out_factor)

                # --------- factor returns ---------
                update_factor_plot_figure1 = returns_plot(factor_returns, self.factor_name)

                update_factor_plot_figure2 = cumulative_return_plot(cumulative_returns, benchmark=self.benchmark,
                                                                    factor_name=self.factor_name)

                # --------- turnover analysis ---------
                turnover = position_turnover(position)
                # display(turnover_analysis(turnover))
                # position graph
                pos_graph = position_plot(position)
                # turnover time series graph
                turnover_ts = turnover_plot(turnover)

                factor_table = pd_to_dash_table(factor_summary(out_factor), 'table')
                ic_table = pd_to_dash_table(pd.DataFrame(calculate_ts_information_coefficient(out_factor, returns),
                                                         columns=[self.factor_name]), 'ic')
                ols_table = pd_to_dash_table(factor_ols_regression(out_factor, returns), 'ols')

                return in_out_distplot, inout_qqplot, \
                       update_factor_plot_figure1, update_factor_plot_figure2, \
                       factor_table, ic_table, ols_table, turnover_ts, pos_graph

        return app


if __name__ == '__main__':
    data = pd.read_csv('../hsi_component.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'code'], inplace=True)
    multi_study = MultiAssetResearch(data)


    def random_alpha(df):
        np.random.seed(0)
        factor = pd.Series(np.random.randn(df.values.shape[0]), index=df.index)
        return factor


    def cheating_alpha(df: pd.DataFrame):
        return df['close'].groupby(level=1).pct_change().groupby(level=1).shift(-1)


    def price_average_alpha(df: pd.DataFrame):
        return df['close'].groupby(level=0).apply(lambda x: (x - x.mean()) / x.std())


    def momentum_alpha(df: pd.DataFrame):
        return df['close'].groupby(level=1).pct_change(5)


    group = {'0001.HK': 1, '0002.HK': 1, '0003.HK': 1, '0005.HK': 1, '0006.HK': 1, '0011.HK': 1,
             '0012.HK': 2, '0016.HK': 2, '0017.HK': 2, '0019.HK': 2, '0066.HK': 2, '0083.HK': 2,
             '0101.HK': 3, '0151.HK': 3, '0175.HK': 3, '0267.HK': 3, '0386.HK': 3, '0388.HK': 3,
             '0669.HK': 4, '0688.HK': 4, '0700.HK': 4, '0762.HK': 4, '0823.HK': 4, '0857.HK': 4,
             '0883.HK': 5, '0939.HK': 5, '0941.HK': 5, '1038.HK': 5, '1044.HK': 5, '1088.HK': 5,
             '1093.HK': 6, '1109.HK': 6, '1177.HK': 6, '1398.HK': 6, '1928.HK': 6, '2007.HK': 6,
             '2018.HK': 7, '2313.HK': 7, '2318.HK': 7, '2319.HK': 7, '2382.HK': 7, '2388.HK': 7,
             '2628.HK': 8, '3328.HK': 8, '3988.HK': 8, '1299.HK': 8, '0027.HK': 8, '0288.HK': 8,
             '1113.HK': 9, '1997.HK': 9}
    multi_study.set_asset_group(group)
    multi_study.calculate_factor(momentum_alpha)
    # multi_study.evaluate_alpha()
    multi_study.get_evaluation_dash_app().run_server('127.0.0.1', debug=True)
    # j = multi_study.factor.reset_index().to_json(orient='index')
    # factor = pd.read_json(j, orient='index', typ='series')
