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


def calculate_cumulative_returns_by_quantile(quantile_ret_ts: pd.DataFrame):
    #                             1_period_return  5_period_return  10_period_return
    # factor_quantile Date
    # 1               2010-06-17         0.002230         0.021172         -0.014775
    #                 2010-06-18         0.036203         0.017436         -0.016843
    #                 2010-06-21        -0.004873        -0.017346         -0.035416
    #                 2010-06-22        -0.000315        -0.036443         -0.046313
    #                 2010-06-23        -0.010813        -0.039430         -0.039475
    # ...                                     ...              ...               ...
    quantile_ret_ts_ = quantile_ret_ts.copy().add(1)  # type: pd.DataFrame
    # todo period larger than 1 is not right cumulative return
    cumulative_ret_by_group = quantile_ret_ts_.groupby(level=0).cumprod()
    cumulative_ret_by_group.dropna(inplace=True)
    cumulative_ret_by_group.sort_index(level=1, inplace=True)
    return cumulative_ret_by_group


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


def calculate_quantile_returns(factor, quantile_lower, quantile_upper) -> pd.Series:
    """

    :param factor:
    :param quantile_lower:
    :param quantile_upper:
    :return:
    """
    factor_df = pd.DataFrame(factor, columns=['quantile_factor'])
    lower_range_ts = factor.groupby(level=0).quantile(quantile_lower)  # type: pd.Series
    lower_range_ts.name = 'lower'
    upper_range_ts = factor.groupby(level=0).quantile(quantile_upper)  # type: pd.Series
    upper_range_ts.name = 'upper'
    factor_df = factor_df.join(lower_range_ts).join(upper_range_ts)
    factor_df['quantile_factor'] = np.where(
        (factor_df['quantile_factor'] >= factor_df['lower']) & (factor_df['quantile_factor'] <= factor_df['upper']),
        factor_df['quantile_factor'], 0)
    return factor_df['quantile_factor']


def quantize_factor(merged_data: pd.DataFrame, quantiles: list = None, bins: int = None):
    """
    merged_data multi index, level 0 is pd.Timestamp, level 1 is asset code.
    two column, factor and 'group'
    :param merged_data:
    :param quantiles:
    :param bins:
    :return:
    """
    merged_data = merged_data.copy().drop_duplicates()
    if not ((quantiles is not None and bins is None) or
            (quantiles is None and bins is not None)):
        raise ValueError('Either quantiles or bins should be provided')

    grouper = [merged_data.index.get_level_values(level=0)]
    if 'group' in merged_data.columns:
        grouper.append('group')

    def quantile_calc(x, _quantiles, _bins):
        if _quantiles is not None and _bins is None:
            return pd.qcut(x, _quantiles, labels=False) + 1
        elif _bins is not None and _quantiles is None:
            return pd.cut(x, _bins, labels=False, duplicates='drop') + 1

    factor_quantile = merged_data.groupby(grouper)['factor'] \
        .apply(quantile_calc, quantiles, bins)
    factor_quantile.name = 'factor_quantile'
    return factor_quantile


def calculate_cross_section_factor_returns(data: pd.DataFrame, position: pd.Series, price_key='close',
                                           factor_name='cross_sectional_factor') -> pd.DataFrame:
    """

    :param data:
    :param position:
    :param price_key:
    :param factor_name:
    :return:
    """

    # todo returns with different holding period
    # first shift the factor by date, because the factor can only decide future return
    shifted_position = position.groupby(level=1).shift(1)
    rate_of_return = data[price_key].groupby(level=1).pct_change()
    # do multiple elementwise
    factor_returns = pd.DataFrame(shifted_position.values * rate_of_return.values, index=rate_of_return.index)
    # sum up the return in the same date.
    factor_returns = factor_returns.groupby(level=0).sum()
    factor_returns.rename({0: factor_name}, axis=1, inplace=True)
    return factor_returns


# here
def calculate_ts_factor_returns(data: pd.DataFrame, factor: pd.Series, periods: list,
                                price_key='close', factor_name='factor') -> pd.DataFrame:
    factor_returns = pd.DataFrame(index=data.index)

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


def get_returns_columns(df: pd.DataFrame) -> list:
    return [col for col in df.columns if '_period_return' in col]


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


def get_valid_quantile(quantile_str: str):
    if quantile_str is None or 'None':
        return None

    ll = list(set([float(q) for q in quantile_str.split(',')]))
    ll.sort()
    if ll[0] > 0:
        ll.insert(0, 0)
    if ll[-1] < 100:
        ll.append(100)
    return ll

