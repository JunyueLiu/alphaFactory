import pandas as pd

from alpha_research import AlphaResearch
from alpha_research.factor_transformation import percentile_factor
from alpha_research.performance_metrics import *
from alpha_research.plotting import *
from alpha_research.utils import *
from IPython.display import display


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
        self.factor_name = 'factor'
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
        summary = pd.DataFrame(factor_summary(self.factor))
        summary.columns = [self.factor_name]

        display(summary)

        # ic table
        ic_table = calculate_information_coefficient(self.factor, returns)
        display(pd.DataFrame(ic_table, columns=[self.factor_name]))

        # factor beta table
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

    def out_of_sample_evaluation(self):


        self.out_of_sample_factor = self.alpha_func(self.out_of_sample, **self.alpha_func_paras)

        t_stat, pvalue = in_out_sample_factor_t_test(self.out_of_sample_factor,
                                                     self.factor[-len(self.out_of_sample_factor):])


        print(t_stat, pvalue)
        overlaid_factor_distribution_plot(self.factor, self.out_of_sample_factor)



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


    def alpha(df, lag_1, lag_2):
        return df['close'].rolling(lag_2).mean() - df['close'].rolling(lag_1).mean()


    factor_study.calculate_factor(alpha, lag_1=5, lag_2=10)
    factor_study.evaluate_alpha()
    factor_study.out_of_sample_evaluation()
