import statsmodels.api as sm
from alpha_research.utils import *


def factor_summary(factor: pd.Series, name='factor') -> pd.DataFrame:
    """

    :param factor:
    :param name:
    :return:
    """
    summary = factor.describe()

    # for SingleAssetResearch
    summary['skewness'] = factor.skew()
    summary['kurtosis'] = factor.kurtosis()
    # t test
    stat, pvalue = stats.ttest_ind(np.zeros_like(factor.values), factor.values, nan_policy='omit')
    summary['t test stat'] = stat
    summary['t test p value'] = pvalue
    # normality test
    stat, pvalue = stats.normaltest(factor.values, nan_policy='omit')
    summary['normality test stat'] = stat
    summary['normality test p value'] = pvalue

    # Augmented Dickey-Fuller test
    if type(factor.index) != pd.MultiIndex:
        # only time series factor has this test
        f = factor.dropna()
        adf = sm.tsa.adfuller(f.values, 1)
        summary['Augmented Dickey-Fuller test stat'] = adf[0]
        summary['Augmented Dickey-Fuller test p value'] = adf[1]
    summary = pd.DataFrame(summary)
    summary.columns = [name]

    return summary


def calculate_ts_information_coefficient(factor, returns, suffix='ic') -> pd.Series:
    """
    :param factor:
    :param returns:
    :param suffix:
    :return:
    """

    _ic = returns \
        .apply(lambda x: stats.spearmanr(x, factor, nan_policy='omit')[0])
    _ic.rename(index={idx: idx + '_' + suffix for idx in _ic.index}, inplace=True)

    return _ic


def calculate_cs_information_coefficient(merged_data: pd.DataFrame, by_group=False,
                                         suffix='ic') -> pd.DataFrame:
    grouper = [merged_data.index.get_level_values(level=0)]
    if 'group' in merged_data.columns and by_group:
        grouper.append('group')

    def src_ic(group):
        f = group['factor']
        _ic = group[get_returns_columns(group)] \
            .apply(lambda x: stats.spearmanr(x, f)[0])
        return _ic

    ic = merged_data.groupby(grouper).apply(src_ic)  # type: pd.DataFrame
    ic.rename(columns={idx: idx + '_' + suffix for idx in ic.columns}, inplace=True)
    return ic


def information_analysis(cross_sectional_ic):
    """

    :param cross_sectional_ic:
    :return:
    """
    ic_summary_table = pd.DataFrame()
    ic_summary_table["IC Mean"] = cross_sectional_ic.mean()
    ic_summary_table["IC Std."] = cross_sectional_ic.std()
    ic_summary_table["Risk-Adjusted IC"] = \
        cross_sectional_ic.mean() / cross_sectional_ic.std()
    t_stat, p_value = stats.ttest_1samp(cross_sectional_ic, 0, nan_policy='omit')
    ic_summary_table["t-stat(IC)"] = t_stat
    ic_summary_table["p-value(IC)"] = p_value
    ic_summary_table["IC Skew"] = stats.skew(cross_sectional_ic, nan_policy='omit')
    ic_summary_table["IC Kurtosis"] = stats.kurtosis(cross_sectional_ic, nan_policy='omit')
    return ic_summary_table.T


def factor_ols_regression(factor, returns: pd.DataFrame) -> pd.DataFrame:
    """

    :param factor:
    :param returns:
    :return:
    """
    result_dic = {}
    for col in returns.columns:
        X = sm.add_constant(factor.values)  # constant is not added by default
        model = sm.OLS(returns[col].values, X, missing='drop')
        result = model.fit()
        d = {}
        d['beta'] = result.params[1]
        d['t value'] = result.tvalues[1]
        d['p value'] = result.pvalues[1]
        result_dic[col] = d
    return pd.DataFrame(result_dic)


def position_turnover(positions: pd.Series):
    """

    :param positions:
    :return:
    """
    # daily turnover
    diff = positions.groupby(level=1).diff(1)  # type: pd.Series
    turnover_ts = diff.groupby(level=0).apply(lambda x: x.abs().sum())  # type: pd.Series
    turnover_ts.name = 'Turnover'
    return turnover_ts


def turnover_analysis(turnover_ts: pd.Series):
    """

    :param turnover_ts:
    :return:
    """
    summary = turnover_ts.describe()
    summary.name = 'Turnover Analysis'
    return summary


def mean_return_by_quantile(merged_data: pd.DataFrame) -> tuple:
    """

    :param merged_data:
    :return:
    """
    grouper = ['factor_quantile', merged_data.index.get_level_values(level=0)]
    # this computes the mean, std, count for each forwards return
    # will generate multi columns output
    #                            1_period_return            ... 10_period_return
    #                                       mean       std  ...              std count
    # factor_quantile  Date
    # 1               2010-06-17        0.002230  0.023423  ...         0.060427    19
    #                 2010-06-18        0.036203  0.026616  ...         0.053852    20
    #                 2010-06-21       -0.004873  0.011273  ...         0.039988    19
    group_stats = merged_data.groupby(grouper)[get_returns_columns(merged_data)] \
        .agg(['mean', 'std', 'count'])

    # quantile_ret_ts
    #   1_period_return  5_period_return  10_period_return
    # factor_quantile Date
    # 1               2010-06-17         0.002230         0.021172         -0.014775
    #                 2010-06-18         0.036203         0.017436         -0.016843
    #                 2010-06-21        -0.004873        -0.017346         -0.035416
    #                 2010-06-22        -0.000315        -0.036443         -0.046313
    quantile_ret_ts = group_stats.T.xs('mean', level=1).T # type: pd.DataFrame


    #              1_period_return            ... 10_period_return
    #                            mean       std  ...              std count
    # factor_quantile                            ...

    group_stats = quantile_ret_ts.groupby(level=0).agg(['mean', 'std', 'count'])
    mean_ret = group_stats.T.xs('mean', level=1).T
    std_error_ret = group_stats.T.xs('std', level=1).T \
                    / np.sqrt(group_stats.T.xs('count', level=1).T)
    return quantile_ret_ts, mean_ret, std_error_ret






def get_monthly_ic(returns: pd.DataFrame, factor: pd.DataFrame, periods: list) -> pd.DataFrame:
    # 先把factor和return合并，再切片
    concat = pd.concat([returns, factor], axis=1)
    concat.rename(columns={'close': 'factor'}, inplace=True)
    columnnames = [str(i) + '_period_return_ic' for i in periods]
    information_coefficient = pd.DataFrame(columns=columnnames)
    year = []
    month = []

    for i in concat.groupby(pd.Grouper(freq='M')):
        # i[0] is timestamp i[1] is dataframe
        # 因为factor这列传进来的是series 没有取名 列名用0来定位

        monthfactor = i[1][0]
        monthreturn = i[1].drop(0, axis=1)

        ic = calculate_ts_information_coefficient(monthfactor, monthreturn)
        information_coefficient = information_coefficient.append(ic, ignore_index=True)

        year.append(str(i[0].year))
        month.append(str(i[0].month))

        information_coefficient['year'] = year
        information_coefficient['month'] = month

    return information_coefficient


def in_out_sample_factor_t_test(insample_factor: pd.Series, out_of_sample_factor: pd.Series):
    return stats.ttest_ind(insample_factor.values, out_of_sample_factor.values, nan_policy='omit')
