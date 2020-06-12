import numpy as np
from graph.factor_component import *


def plot_returns():
    pass

def plot_factor_distribution():
    pass

if __name__ == '__main__':
    period = [1, 5]
    df = pd.read_csv(
        '/Users/liujunyue/PycharmProjects/ljquant/hkex_data/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv')
    df.set_index('time_key', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[-100:]
    # returns = calculate_returns(df, period)
    # infer_factor_time_frame(df)
    factor = 1 / (1 + np.exp(-df['close'] + df['close'].shift(1)))