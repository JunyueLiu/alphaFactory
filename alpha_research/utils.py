import pandas as pd
from scipy import stats
import numpy as np


from alpha_research.performance_metrics import calculate_information_coefficient, factor_ols_regression


def calculate_returns(data: pd.DataFrame, periods: list, price_key='close') -> pd.DataFrame:
    # 取了两个周期 periods=[1,2] shift 1天和2天
    returns = pd.DataFrame(index=data.index)
    for period in periods:
        returns[str(period) + '_period_return'] = df[price_key].pct_change(periods=period).shift(-period)
    return returns

#here
def factor_returns(returns: pd.DataFrame, factor:pd.DataFrame, periods: list, price_key='close')-> pd.DataFrame:
    factorReturns = pd.DataFrame(index=returns.index)
    for period in periods:
        factorReturns[str(period) + '_period_return']=factor
        i = 1
        while i < len(factor):
            if(i%period != 0):
                factorReturns[str(period) + '_period_return'][i]=0
            i += 1
        print(factorReturns[str(period) + '_period_return'])


        factorReturns[str(period) + '_period_return']\
            *= returns[str(period) + '_period_return']*10000

    return factorReturns





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
    #打印不省略部分列
    pd.set_option('display.max_rows', None)

    period=[1,5]
    df = pd.read_csv('/Users/silviaysy/Desktop/project/alphaFactory/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv')
    df.set_index('time_key', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[-100:]
    returns = calculate_returns(df, period)
    infer_factor_time_frame(df)
    factor = 1 / (1 + np.exp(-df['close'] + df['close'].shift(1)))
    factorreturns = factor_returns(returns,factor,period)
    print(factorreturns)

    # #Information Coefficient
    # ic = calculate_information_coefficient(factor, returns)
    # results = factor_ols_regression(factor, returns)

