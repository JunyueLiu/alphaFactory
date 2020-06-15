import pandas as pd
import numpy as np
from alpha_research import AlphaResearch
from alpha_research.utils import infer_factor_time_frame,calculate_forward_returns


class MultiAssetResearch(AlphaResearch):
    """


    """

    def __init__(self, data: pd.DataFrame, out_of_sample: pd.DataFrame = None, split_ratio: float = 0.3,
                 factor_parameters=None):
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

    def calculate_factor(self, func, **kwargs):
        self.alpha_func = func
        self.alpha_func_paras = kwargs
        if kwargs is not None:
            factor = func(self.in_sample, **kwargs)
            assert np.array_equal(factor.index == self.in_sample.index)
            assert factor.value.shape[0] == self.in_sample.shape[0]
        else:
            factor = func(self.in_sample)
            assert np.array_equal(factor.index == self.in_sample.index)
            assert factor.value.shape[0] == self.in_sample.shape[0]
        self.factor = factor


    def evaluate_alpha(self):
        pass


if __name__ == '__main__':
    data = pd.read_csv('../hsi_multiasset_sample.csv')
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'code'], inplace=True)
    multi_study = MultiAssetResearch(data)


    def random_alpha(df):
        np.random.seed(0)
        factor = pd.DataFrame(np.random.randint(-10, 10, df.values.shape[0]), index=df.index)
        return factor


    factor = random_alpha(data)
    fr = calculate_forward_returns(data, [1, 2, 3])
