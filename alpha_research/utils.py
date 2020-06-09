import pandas as pd
from scipy import stats
import numpy as np

from alpha_research.performance_metrics import calculate_information_coefficient, factor_ols_regression


def calculate_returns(data: pd.DataFrame, periods: list, price_key='close') -> pd.DataFrame:
    returns = pd.DataFrame(index=data.index)
    for period in periods:
        returns[str(period) + '_period_return'] = df[price_key].pct_change(periods=period).shift(-period)
    return returns

def factor_returns(factor):
    pass


def get_returns_columns()->list:
    pass






def infer_factor_time_frame(data: pd.DatetimeIndex):
    time_delta = data.index[1:] - data.index[:-1]
    # get mode using scipy
    td = stats.mode(time_delta)[0][0]
    td = td.astype('timedelta64[m]')

    minutes = td / np.timedelta64('1', 'm')

    if minutes < 60:
        return str(int(minutes)) + 'm'
    elif minutes < 1440:
        return str(int(minutes / 60)) + 'H'
    elif minutes < 7200:
        return str(int(minutes / 1440)) + 'D'
    elif minutes < 28800:
        return str(int(minutes / 7200)) + 'W'
    else:
        return str(int(minutes / 28800)) + 'M'


if __name__ == '__main__':
    df = pd.read_csv()
    df.set_index('time_key', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[-100:]
    returns = calculate_returns(df, [1,2])
    # infer_factor_time_frame(df)
    factor = df['close'] - df['close'].shift(1)
    ic = calculate_information_coefficient(factor, returns)
    results = factor_ols_regression(factor, returns)
