import pandas as pd
from scipy import stats
import numpy as np


def calculate_forward_returns(data: pd.DataFrame, periods: list, price_key='close') -> pd.DataFrame:
    # 取了两个周期 periods=[1,2] shift 1天和2天
    returns = pd.DataFrame(index=data.index)
    for period in periods:
        if type(data.index) == pd.MultiIndex:
            def multi_index_forward_returns(df: pd.DataFrame):
                return df[price_key].pct_change(periods=period).shift(-period)

            tmp = data.groupby(level=1).apply(multi_index_forward_returns).droplevel(0)
            returns[str(period) + '_period_return'] = tmp
        else:
            returns[str(period) + '_period_return'] = data[price_key].pct_change(periods=period).shift(-period)
    return returns


def calculate_cumulative_returns(returns, starting_value=0, out=None):
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


def calculate_position(factor: pd.Series):
    """
    The position of cross sectional alpha is calculated by
    alpha / (sum(abs(alpha)))
    The sum means the sum of alpha cross sectional, which means in the same time stamp.
    For example,
    Date        code
    2010-06-15  0001.HK   2
                0011.HK   5
                0027.HK -10
                1398.HK  -7
                1928.HK  -7
                2318.HK  -3
    summation = |2| + |5| + |-10| + |-7| + |-7| + |-3|= 34

    :param factor:
    :return:
    """
    return factor.groupby(level=0).apply(lambda x: x / x.abs().sum())


def trading_basket(last_position, alpha):
    pass

def calculate_quantile_returns(factor, quantile):
    pass

# here
def calculate_factor_returns(data: pd.DataFrame, factor: pd.DataFrame, periods: list,
                             price_key='close', factor_name='factor') -> pd.DataFrame:
    factor_returns = pd.DataFrame(index=data.index)
    # for cross sectional factor
    if type(factor_returns.index) == pd.MultiIndex:
        # todo returns with different holding period
        # calculate position by factor weight
        position = calculate_position(factor)
        # first shift the factor by date, because the factor can only decide future return
        shifted_position = position.groupby(level=1).shift(1)
        rate_of_return = data[price_key].groupby(level=1).pct_change()
        # do multiple elementwise
        factor_returns = pd.DataFrame(shifted_position.values * rate_of_return.values, index=rate_of_return.index)
        # sum up the return in the same date.
        factor_returns = factor_returns.groupby(level=0).sum()
        factor_returns.rename({0: factor_name}, axis=1, inplace=True)
    else:
        # for time series factor
        for period in periods:
            factor_returns[str(period) + '_period_factor'] = factor.copy()
            # force the factor to in the range of -1 and 1
            factor_returns[str(period) + '_period_factor'] = np.clip(factor_returns[str(period) + '_period_factor'], -1,
                                                                     1)

            if period > 1:
                # find the first non nan value to identify where the multi step factor starts
                i = np.argwhere(np.isnan(factor.values) == False)[0][0]
                factor_returns['a'] = 0
                factor_returns.iloc[i:]['a'] = 1
                factor_returns.iloc[i:]['a'] = (factor_returns['a'].iloc[i:].cumsum() - 1).mod(period)
                # for factor trying to predict multi steps, the factor position will be fixed until time period end
                factor_returns[str(period) + '_period_factor'] = np.where(factor_returns['a'] == 0,
                                                                          factor_returns[
                                                                              str(period) + '_period_factor'],
                                                                          np.nan)
                factor_returns[str(period) + '_period_factor'].fillna(method='ffill', inplace=True)
                del factor_returns['a']
            factor_returns[str(period) + '_period_factor'] = factor_returns[str(period) + '_period_factor'].shift(1)
            ret = data[price_key].pct_change()
            factor_returns[str(period) + '_period_factor'] *= ret
    return factor_returns


def get_returns_columns() -> list:
    pass


def infer_factor_time_frame(data: pd.DatetimeIndex):
    # fix bug
    # This is to deal with multiIndex case, which the datetimeIndex is not unique
    unique_index = np.unique(data.values)
    unique_index.sort()
    time_delta = unique_index[1:] - unique_index[:-1]
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


def infer_break(data: pd.DataFrame):
    dt_range = pd.date_range(data.index[0], data.index[-1], freq=infer_factor_time_frame(data.index))
    return [dt for dt in dt_range if dt not in data.index]


def generate_strftime_format(index):
    tf = infer_factor_time_frame(index)
    if 'min' in tf or 'H' in tf:
        return '%Y/%m/%d %H:%M:%S'
    else:
        return '%Y/%m/%d'






if __name__ == '__main__':
    # 打印不省略部分列
    # pd.set_option('display.max_rows', None)

    period = [1]
    df = pd.read_csv(
        '/Users/silviaysy/Desktop/project/alphaFactory/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv')
    df.set_index('time_key', inplace=True)
    df.index = pd.to_datetime(df.index)
    df = df[-100:]

    returns = calculate_forward_returns(df, period)

    infer_factor_time_frame(df)

    # 目前造的factor是根据两天的收盘价 这个可以变
    factor = 1 / (1 + np.exp(-df['close'] + df['close'].shift(1)))

    factorreturns = calculate_factor_returns(df, factor, period)
    # print(factorreturns)

    cumulatereturns = calculate_cumulative_returns(factorreturns, 1)
    #   print(cumulatereturns)

    # #Information Coefficient
    # ic = calculate_information_coefficient(factor, returns)
    # print(ic)
# results = factor_ols_regression(factor, returns)
