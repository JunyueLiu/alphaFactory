import pandas as pd
import numpy as np
from IPython.core.display import display

from alpha_research import AlphaResearch
from alpha_research.plotting import factor_distribution_plot, qq_plot, returns_plot, cumulative_return_plot
from alpha_research.utils import infer_factor_time_frame, calculate_forward_returns, calculate_factor_returns, \
    calculate_position, calculate_cumulative_returns
from alpha_research.performance_metrics import calculate_information_coefficient, factor_summary, factor_ols_regression

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
        else:
            if list(data.colums) != list(out_of_sample.columns):
                raise AttributeError('The in the sample data and the out of sample data should have same columns')
            self.in_sample = data
            self.out_of_sample = out_of_sample

        self.factor_parameter = factor_parameters
        self.factor = None
        self.out_of_sample_factor = None
        self.factor_timeframe = infer_factor_time_frame(self.in_sample.index.get_level_values(0))
        self.factor_name = 'Cross Sectional Factor'
        self.factor_percentile_entry = 0.8
        self.alpha_func = None
        self.alpha_func_paras = None

        if benchmark is not None:
            # todo compare the index in the benchmark and the first level of the index
            # make sure the benchmark contains the date in the first level of the index
            self.benchmark = benchmark
        else:
            self.benchmark = benchmark

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

        # factor
        factor_returns = calculate_factor_returns(self.in_sample, self.factor, forward_return_lag)
        fig = returns_plot(factor_returns, self.factor_name)
        fig.show()


        cumulative_returns = calculate_cumulative_returns(factor_returns, 1)
        fig = cumulative_return_plot(cumulative_returns, benchmark=self.benchmark, factor_name=self.factor_name)
        fig.show()

        # position time series of each asset

        # return by factor bin

        #




if __name__ == '__main__':
    data = pd.read_csv('../hsi_component.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'code'], inplace=True)
    multi_study = MultiAssetResearch(data)


    def random_alpha(df):
        np.random.seed(0)
        factor = pd.Series(np.random.randn(df.values.shape[0]), index=df.index)
        return factor


    multi_study.calculate_factor(random_alpha)
    multi_study.evaluate_alpha()
