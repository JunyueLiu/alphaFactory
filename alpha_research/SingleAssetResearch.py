import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

from alpha_research import AlphaResearch
from alpha_research.factor_transformation import percentile_factor
from alpha_research.performance_metrics import *
from alpha_research.plotting import *
from alpha_research.utils import *
from alpha_research.factor_zoo import *
from IPython.display import display

# import plotly.io as pio

#####xlwww
# pio.renderers.default = "browser"


class SingleAssetResearch(AlphaResearch):
    """


    """

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
            self.factor = func(self.in_sample, **kwargs)
        else:
            self.factor = func(self.in_sample)

    def evaluate_alpha(self, forward_return_lag: list = None):

        if forward_return_lag is None:
            forward_return_lag = [1, 5, 10]
        returns = calculate_forward_returns(self.in_sample, forward_return_lag)
        # in sample
        # factor summary
        summary = factor_summary(self.factor, self.factor_name)
        pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x))
        display(summary)

        # ic table
        ic_table = calculate_information_coefficient(self.factor, returns)
        pd.set_option('display.float_format', lambda x: '{:.5f}'.format(x))
        display(pd.DataFrame(ic_table, columns=[self.factor_name]))

        # factor beta table
        pd.set_option('display.float_format', None)
        ols_table = factor_ols_regression(self.factor, returns)
        display(ols_table)
        # factor distribution plot
        fig = factor_distribution_plot(self.factor)
        fig.show()
        fig = qq_plot(self.factor)
        fig.show()

        # factor backtesting
        fig = price_factor_plot(self.in_sample, self.factor)
        fig.show()
        factor_returns = calculate_factor_returns(self.in_sample, self.factor, forward_return_lag)
        fig = returns_plot(factor_returns, self.factor_name)
        fig.show()
        cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
        benchmark = self.in_sample['close'] / self.in_sample['close'][0]
        fig = cumulative_return_plot(cumulative_returns, benchmark=benchmark, factor_name=self.factor_name)
        fig.show()
        per_factor = percentile_factor(self.factor, self.factor_percentile_entry)
        fig = entry_and_exit_plot(self.in_sample, per_factor)
        fig.show()

        # todo according infer timeframe of the factor to generate heatmap

    def out_of_sample_evaluation(self):

        self.out_of_sample_factor = self.alpha_func(self.out_of_sample, **self.alpha_func_paras)

        t_stat, pvalue = in_out_sample_factor_t_test(self.out_of_sample_factor,
                                                     self.factor[-len(self.out_of_sample_factor):])

        # print(t_stat, pvalue)
        fig = overlaid_factor_distribution_plot(self.factor, self.out_of_sample_factor)
        fig.show()

    def get_evaluation_dash_app(self):
        """

        :return:
        """
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        forward_returns_period = [1, 2, 5, 10]
        forward_str = str(forward_returns_period).replace('[', '').replace(']', '')
        app.layout = html.Div(children=[
            html.H1(children=self.factor_name + ' evaluation'),
            html.Div([
                html.Div(id='forward-returns-period'),
                html.Br(),
                # add forward returns
                html.Div(children='Enter a value to add or remove forward return value'),
                dcc.Input(
                    id='forwards-periods-input',
                    # placeholder='Enter values, split by ,',
                    type='text',
                    value=forward_str
                ),
                html.Button('Update', id='UpdateButton'), ]
                , style={'width': '49%', 'display': 'inline-block'}),
            # change parameter
            html.Div([
                html.Div(children='Factor Parameter'),
                html.Div([
                    dcc.Input(
                        id="input_{}".format(k),
                        placeholder=str(k),
                        type='number',
                        value=str(v), debounce=True
                    ) for k, v in self.alpha_func_paras.items()
                ]),
                html.Button('Submit', id='button'),
                html.Div(id="current-parameter"),
            ], style={'width': '49%', 'display': 'inline-block'}),
            html.Div([
                dcc.RadioItems(
                    id='in-out-sample',
                    options=[{'label': i, 'value': i} for i in ['In sample', 'Out ot the sample']],
                    value='In sample',
                    labelStyle={'display': 'inline-block'}
                )

            ]),
            html.Div([html.Div(children='Factor Distribution'), dcc.Graph(id='distribution')],
                     style={'width': '49%', 'display': 'inline-block'}),
            html.Div([html.Div(children='Q-Q plot '), dcc.Graph(id='qqplot')],
                     style={'width': '49%', 'display': 'inline-block'}),
            html.Div([html.Div(children='Price Factor'),
                      dcc.Graph(id='price_factor')],
                     style={'width': '100%', 'display': 'inline-block'}),
            html.Div([html.Div(children='Factor Return'),
                      dcc.Graph(id='factor-returns')],
                     style={'width': '100%', 'display': 'inline-block'}),
            html.Div([html.Div(children='Factor Backtesting'),
                      dcc.Graph(id='factor-backtest')],
                     style={'width': '100%', 'display': 'inline-block'}),
        ])

        @app.callback(Output("forward-returns-period", "children"),
                      [Input("UpdateButton", "n_clicks")],
                      [State("forwards-periods-input", "value")])
        def add_forward_returns(n_clicks, s: str):
            try:
                global forward_returns_period
                global forward_str
                if s.strip() == '':
                    forward_returns_period = []
                    return 'Forward return list: '

                forward_returns_period = list(set([int(p) for p in s.split(',')]))
                forward_returns_period.sort()
                forward_str = str(forward_returns_period).replace('[', '').replace(']', '')
                return 'Forward return list: ' + forward_str
            except:
                return 'Update Failed, please check your input. Forward return list: ' + forward_str

        @app.callback(
            Output('distribution', 'figure'),
            [Input('in-out-sample', 'value')])
        def update_distribution_figure(value):
            if value == 'In sample':
                return factor_distribution_plot(self.factor)
            else:
                return factor_distribution_plot(self.out_of_sample_factor)

        @app.callback(
            Output('qqplot', 'figure'),
            [Input('in-out-sample', 'value')])
        def update_qqplot_figure(value):
            if value == 'In sample':
                return qq_plot(self.factor)
            else:
                return qq_plot(self.out_of_sample_factor)

        @app.callback(
            Output('price_factor', 'figure'),
            [Input('in-out-sample', 'value')])
        def update_factor_plot_figure(value):
            if value == 'In sample':
                return price_factor_plot(self.in_sample, self.factor)
            else:
                return price_factor_plot(self.out_of_sample, self.out_of_sample_factor)

        @app.callback(
            Output('factor-returns', 'figure'),
            [Input('in-out-sample', 'value')])
        def update_factor_plot_figure(value):
            # global forward_returns_period
            if value == 'In sample':
                factor_returns = calculate_factor_returns(self.in_sample, self.factor, forward_returns_period)
                return returns_plot(factor_returns, self.factor_name)
            else:
                return None

        @app.callback(
            Output('factor-backtest', 'figure'),
            [Input('in-out-sample', 'value')])
        def update_factor_plot_figure(value):
            # global forward_returns_period
            if value == 'In sample':
                factor_returns = calculate_factor_returns(self.in_sample, self.factor, forward_returns_period)
                cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
                benchmark = self.in_sample['close'] / self.in_sample['close'][0]
                return cumulative_return_plot(cumulative_returns, benchmark=benchmark, factor_name=self.factor_name)
            else:
                return None

        return app


class DemoSingleAssetFactor(SingleAssetResearch):
    def __init__(self, data: pd.DataFrame, out_of_sample: pd.DataFrame = None, split_ratio: float = 0.3,
                 factor_parameters=None):
        super(DemoSingleAssetFactor, self).__init__(data, out_of_sample, split_ratio, factor_parameters)


if __name__ == '__main__':
    data_path = '/Users/liujunyue/PycharmProjects/alphaFactory/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'

    df = pd.read_csv(data_path)
    df['time_key'] = pd.to_datetime(df['time_key'])
    df.set_index('time_key', inplace=True)
    df = df[-500:]
    parameter = {'short_period': 5, 'long_period': 10}
    factor_study = SingleAssetResearch(df)

    factor_study.calculate_factor(alpha_6, time_lag=5)
    factor_study.evaluate_alpha()
    # factor_study.out_of_sample_evaluation()
    factor_study.get_evaluation_dash_app().run_server(debug=True)
