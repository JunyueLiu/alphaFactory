import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResults


def factor_summary(factor:pd.DataFrame):
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
    stat, pvalue =stats.normaltest(factor.values, nan_policy='omit')
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


def factor_ols_regression(factors, returns: pd.DataFrame) -> [RegressionResults]:
    #to do make the RegressionResult to pd.DataFrame

    result_list = []
    for col in returns.columns:
        X = sm.add_constant(factors.values) # constant is not added by default
        model = sm.OLS(returns[col].values, X, missing='drop')
        result = model.fit()
        result_list.append(result)
    return result_list


