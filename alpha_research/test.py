from alpha_research.utils import *
from alpha_research.plotting import *
from alpha_research.factor_transformation import *
from alpha_research.performance_metrics import *

import pandas as pd

if __name__ == '__main__':
    # 打印不省略部分列
    # pd.set_option('display.max_rows', None)
    data_path = '/Users/liujunyue/PycharmProjects/alphaFactory/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'

    period = [1, 2, 5, 10]
    df = pd.read_csv(data_path)
    df.set_index('time_key', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[-10000:]

    returns = calculate_forward_returns(df, period)

    # 目前造的factor是根据两天的收盘价 这个可以变
    factor = 1 / (1 + np.exp(-df['close'] + df['close'].shift(1)))
    d = factor_ols_regression(factor, returns)

    # factorreturns = calculate_factor_returns(df, factor, period)
    # print(factorreturns)

    # cumulatereturns = calculate_cumulative_returns(factorreturns, 1)
    # dt_break = infer_break(df)

    # infer_factor_time_frame(data)
    # per_factor = percentile_factor(factor, 0.8)
    # fig = factor_distribution_plot(factor)
    # fig.show()
    # summary = factor_summary(factor)
    # benchmark = df['close'] / df['close'][0]
    # fig = cumulative_return_plot(cumulatereturns, benchmark)
    # fig.show()qq_plot(factor).show()
    # qq_plot(factor).show()