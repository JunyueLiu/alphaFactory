import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.regression.linear_model import RegressionResults


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
    # todo make the RegressionResult to pd.DataFrame
    result_list = []
    for col in returns.columns:
        X = sm.add_constant(factors.values) # constant is not added by default
        model = sm.OLS(returns[col].values, X, missing='drop')
        result = model.fit()
        result_list.append(result)
    return result_list


