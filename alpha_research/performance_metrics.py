import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm


def factor_summary(factor: pd.DataFrame):
    """

    :param factor:
    :return:
    """
    summary = factor.describe()
    summary['skewness'] = summary.skew()
    summary['kurtosis'] = summary.kurtosis()
    # t test
    stat, pvalue = stats.ttest_ind(np.zeros_like(factor.values), factor.values, nan_policy='omit')
    summary['t test stat'] = stat
    summary['t test p value'] = pvalue
    # normality test
    stat, pvalue = stats.normaltest(factor.values, nan_policy='omit')
    summary['normality test stat'] = stat
    summary['normality test p value'] = pvalue

    # Augmented Dickey-Fuller test
    f = factor.dropna()
    adf = sm.tsa.adfuller(f.values, 1)
    summary['Augmented Dickey-Fuller test stat'] = adf[0]
    summary['Augmented Dickey-Fuller test p value'] = adf[1]
    return summary


def calculate_information_coefficient(factor, returns, suffix='ic') -> pd.Series:
    """
    :param factor:
    :param returns:
    :param suffix:
    :return:
    """

    _ic = returns \
        .apply(lambda x: stats.spearmanr(x, factor, nan_policy='omit')[0])

    return _ic.rename(index={idx: idx + '_' + suffix for idx in _ic.index})


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


def in_out_sample_factor_t_test(insample_factor: pd.Series, out_of_sample_factor: pd.Series):
    return stats.ttest_ind(insample_factor.values, out_of_sample_factor.values, nan_policy='omit')
