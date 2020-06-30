import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np
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
            self.alpha_universe = self.in_sample.index.get_level_values(level=1)
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
            factor = func(self.in_sample)
            assert type(factor) == pd.Series
            assert np.array_equal(factor.index, self.in_sample.index)
            assert factor.values.shape[0] == self.in_sample.shape[0]
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
        merged_data = self.merged_data.join(returns) # type: pd.DataFrame
        # in sample
        # factor summary
        summary = factor_summary(self.factor, self.factor_name)
        pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))
        display(summary)

        # ic table

        ic = calculate_cs_information_coefficient(merged_data)
        pd.set_option('display.float_format', lambda x: '{:.5f}'.format(x))
        display(information_analysis(ic))

        # factor beta table
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

        # factor returns
        factor_returns = calculate_cross_section_factor_returns(self.in_sample, position)
        fig = returns_plot(factor_returns, self.factor_name)
        fig.show()

        cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
        fig = cumulative_return_plot(cumulative_returns, benchmark=self.benchmark, factor_name=self.factor_name)
        fig.show()

        ## turnover analysis
        turnover = position_turnover(position)
        display(turnover_analysis(turnover))
        # position graph
        fig = position_plot(position)
        fig.show()
        # turnover time series graph
        fig = turnover_plot(turnover)
        fig.show()

        ## Return analysis
        # return by factor bin
        factor_quantile = quantize_factor(merged_data, self.factor_quantile_list, self.factor_bin_num) # type: pd.Series
        merged_data['factor_quantile'] = factor_quantile
        quantile_ret_ts, mean_ret, std_error_ret = mean_return_by_quantile(merged_data)
        display(mean_ret)

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
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        app.layout = html.Div(children=[
            html.H1(children=self.factor_name + ' evaluation',
                    style={'font-weight': 'normal', 'text-align': 'center', 'display': 'block',
                           'fontFamily': 'helvetica neue', 'margin': '100px auto'}),
            html.Div([
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

    def momentum_alpha(df:pd.DataFrame):
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
    multi_study.evaluate_alpha()
