import pandas as pd
from scipy import stats
import numpy as np
from alpha_research.performance_metrics import calculate_information_coefficient, factor_ols_regression


def forward_returns(data: pd.DataFrame, periods: list, price_key='close') -> pd.DataFrame:
    # 取了两个周期 periods=[1,2] shift 1天和2天
    returns = pd.DataFrame(index=data.index)
    for period in periods:
        returns[str(period) + '_period_return'] = data[price_key].pct_change(periods=period).shift(-period)
    return returns


def cumulative_returns(returns, starting_value=0, out=None):
    if len(returns) < 1:
        return returns.copy()

    nanmask = np.isnan(returns)
    if np.any(nanmask):
        returns = returns.copy()
        returns[nanmask] = 0

    allocated_output = out is None
    if allocated_output:
        out = np.empty_like(returns)

    np.add(returns, 1, out=out)
    out.cumprod(axis=0, out=out)

    if starting_value == 0:
        np.subtract(out, 1, out=out)
    else:
        np.multiply(out, starting_value, out=out)

    if allocated_output:
        if returns.ndim == 1 and isinstance(returns, pd.Series):
            out = pd.Series(out, index=returns.index)
        elif isinstance(returns, pd.DataFrame):
            out = pd.DataFrame(
                out, index=returns.index, columns=returns.columns,
            )

    return out


# here
def factor_returns(data: pd.DataFrame, factor: pd.DataFrame, periods: list, price_key='close') -> pd.DataFrame:
    factorReturns = pd.DataFrame(index=data.index)
    for period in periods:
        factorReturns[str(period) + '_period_factor'] = factor.copy()

        # factorReturns[str(period) + '_period_factor'].fillna(value=0, inplace=True)
        # i = 0
        # while i < len(factor):
        #     if (i  % period != 0):
        #         factorReturns[str(period) + '_period_factor'][i] = np.nan
        #     i += 1
        if period > 1:
            # find the first non nan value to identify where the multi step factor starts
            i = np.argwhere(np.isnan(factor.values) == False)[0][0]
            factorReturns['a'] = 0
            factorReturns.iloc[i:]['a'] = 1
            factorReturns.iloc[i:]['a'] = (factorReturns['a'].iloc[i:].cumsum() - 1).mod(period)
            # for factor trying to predict multi steps, the factor position will be fixed until time period end
            factorReturns[str(period) + '_period_factor'] = np.where(factorReturns['a'] == 0,
                                                                     factorReturns[str(period) + '_period_factor'],
                                                                     np.nan)
            factorReturns[str(period) + '_period_factor'].fillna(method='ffill', inplace=True)
            del factorReturns['a']
        factorReturns[str(period) + '_period_factor'] = factorReturns[str(period) + '_period_factor'].shift(1)
        ret = data[price_key].pct_change()
        factorReturns[str(period) + '_period_factor'] *= ret
    return factorReturns


def get_returns_columns() -> list:
    pass


def infer_factor_time_frame(data: pd.DatetimeIndex):
    time_delta = data.values[1:] - data.values[:-1]
    # get mode using scipy
    td = stats.mode(time_delta)[0][0]
    td = td.astype('timedelta64[m]')

    minutes = td / np.timedelta64('1', 'm')

    if minutes < 60:
        return str(int(minutes)) + 'min'
    elif minutes < 1440:
        return str(int(minutes / 60)) + 'H'
    elif minutes < 7200:
        return str(int(minutes / 1440)) + 'D'
    elif minutes < 28800:
        return str(int(minutes / 7200)) + 'W'
    else:
        return str(int(minutes / 28800)) + 'M'

def infer_break(data:pd.DataFrame):
    dt_range = pd.date_range(data.index[0], data.index[-1], freq=infer_factor_time_frame(data.index))
    return [dt for dt in dt_range if dt not in data.index]


if __name__ == '__main__':
    # 打印不省略部分列
    # pd.set_option('display.max_rows', None)

    period = [1, 2]
    df = pd.read_csv('/Users/liujunyue/PycharmProjects/alphaFactory/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv')
    df.set_index('time_key', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[-100:]

    returns = forward_returns(df, period)

    infer_factor_time_frame(df)

    # 目前造的factor是根据两天的收盘价 这个可以变
    factor = 1 / (1 + np.exp(-df['close'] + df['close'].shift(1)))

    factorreturns = factor_returns(df, factor, period)
    # print(factorreturns)

    cumulatereturns = cumulative_returns(factorreturns, 1)
#   print(cumulatereturns)

# #Information Coefficient
# ic = calculate_information_coefficient(factor, returns)
# results = factor_ols_regression(factor, returns)
