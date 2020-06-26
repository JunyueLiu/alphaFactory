"""
Aim to contain some studied factor in the literature

"""
import pandas as pd
import numpy as np
from scipy import stats


def alpha_1():
    pass



def alpha_6(df: pd.DataFrame, time_lag=10):
    factor = -1 * df['open'].rolling(time_lag).corr(df['volume'])
    return factor


def alpha_9(df: pd.DataFrame, time_shift=1, rolling_windows = 5):
    condition = (df['close'] - df['close'].shift(time_shift)).rolling(rolling_windows).min()
    condition2 = (df['close'] - df['close'].shift(time_shift)).rolling(rolling_windows).max()
    ans1 = df['close'] - df['close'].shift(1)
    factor = np.where(condition > 0, ans1, np.where(condition2 < 0, ans1, -1 * ans1))
    # print(factor)
    return factor


def alpha_12(df: pd.DataFrame, time_lag=1):
    factor = np.sign(df['volume'] - df['volume'].shift(1)) * (-1 * (df['close'] - df['close'].shift(1)))
    # print(factor)
    return factor


def alpha_21(df: pd.DataFrame):
    condition1 = df['close'].rolling(8).mean() + df['close'].rolling(8).std()
    condition2 = df['close'].rolling(2).mean()
    condition3 = df['close'].rolling(8).mean() - df['close'].rolling(8).std()
    condition4 = df['volume'] / df['volume'].rolling(20).mean()
    factor = np.where(condition1 < condition2, -1,
                      np.where(condition2 < condition3, 1, np.where(condition4 >= 1, 1, -1)))
    # print(factor)
    return factor


def alpha_23(df: pd.DataFrame, time_lag=20):
    tmp = df['high'].rolling(time_lag).mean()
    factor = np.where(df['high'] > tmp, -1 * (df['high'] - df['high'].shift(2)), 0)
    return factor


def alpha_24(df: pd.DataFrame):
    delta_sum = df['close'].rolling(100).mean()
    delta_sum = delta_sum - delta_sum.shift(100)
    delay_close = df['close'].shift(100)
    tmp1 = delta_sum / delay_close
    ts_min = df['close'].rolling(100).min()
    factor = np.where(tmp1 <= 0.05, df['close'] - ts_min, df['close'] - df['close'].shift(3))
    return factor


def alpha_26(df: pd.DataFrame):
    factor = []
    return factor


def alpha_28(df: pd.DataFrame):
    factor = []
    return factor


def alpha_32(df: pd.DataFrame):
    factor = []
    return factor


def alpha_35(df: pd.DataFrame):
    factor = []
    return factor


def alpha_41(df: pd.DataFrame):
    vwap = (np.cumsum(df['volume'] * df['close']) / np.cumsum(df['volume']))
    factor = np.power(df['high'] * df['low'], 0.5) - vwap
    return factor


# def alpha_43(df:pd.DataFrame):
#     tmp1 = df['volume'] / df['volume'].rolling(20).mean()
#     rank1 = tmp1.rank()
#     rank2 = -1 * (df['close'] - df['close'].shift(7)).rank()

def alpha_46(df: pd.DataFrame):
    condition = (df['close'].shift(20) - df['close'].shift(10)) / 10 - (df['close'].shift(10) - df['close']) / 10
    factor = np.where(condition > 0.25, -1, np.where(condition < 0, 1, -1 * (df['close'] - df['close'].shift(1))))
    return factor


def alpha_49(df: pd.DataFrame):
    condition = (df['close'].shift(20) - df['close'].shift(10)) / 10 - (df['close'].shift(10) - df['close']) / 10
    factor = np.where(condition < -0.1, 1, (-1 * (df['close'] - df['close'].shift(1))))
    return factor


def alpha_51(df: pd.DataFrame):
    condition = (df['close'].shift(20) - df['close'].shift(10)) / 10 - (df['close'].shift(10) - df['close']) / 10
    factor = np.where(condition < -0.05, 1, -1 * (df['close'] - df['close'].shift(1)))
    return factor


def alpha_53(df: pd.DataFrame):
    tmp = (df['close'] - df['low']) / (df['close'] - df['low'])
    factor = -1 * (tmp - tmp.shift(9))
    return factor


def alpha_54(df: pd.DataFrame):
    factor = (-1 * ((df['low'] - df['close']) * np.power(df['open'], 5)) / (
                (df['low'] - df['high']) * np.power(df['close'], 5)))
    # print(factor)
    return factor


def alpha_84(df: pd.DataFrame):
    # SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close, 4.96796))
    return


def alpha_101(df: pd.DataFrame):
    factor = (df['close'] - df['open']) / ((df['high'] - df['low']) + 0.001)
    # print(factor)
    return factor


if __name__ == '__main__':
    df = pd.read_csv('../data.csv').head(200)
    # print(alpha_6(df))
    alpha_21(df)
