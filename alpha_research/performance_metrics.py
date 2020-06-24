import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from scipy import stats
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
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


def calculate_information_coefficient(factor, returns, suffix='ic') -> pd.Series:
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

        ic = calculate_information_coefficient(monthfactor, monthreturn)
        information_coefficient = information_coefficient.append(ic, ignore_index=True)

        year.append(str(i[0].year))
        month.append(str(i[0].month))

        information_coefficient['year'] = year
        information_coefficient['month'] = month

    return information_coefficient


def plot_monthly_ic_heatmap(mean_monthly_ic):
    mean_monthly_ic = mean_monthly_ic.copy()

    # 给原来df的添加一个index,便于后面搜索
    mean_monthly_ic = mean_monthly_ic \
        .set_index([mean_monthly_ic['year'], mean_monthly_ic['month']])
    print(mean_monthly_ic)

    # 设定集合
    x = [str(i) for i in range(1, 13)]  # month
    y = list(set([int(i) for i in mean_monthly_ic['year']]))  # year 去重
    y.sort(reverse=True)

    mean_monthly_ic = mean_monthly_ic.drop(columns=['month', 'year'])
    print(mean_monthly_ic)
    # heatmap的z
    z = list()
    # heatmap titles
    titles = list()

    for i in mean_monthly_ic.iteritems():
        titles.append(i[0])

        z_year = list()
        for year in y:
            z_month = list()
            for month in x:
                try:
                    ic = i[1].loc[str(year), str(month)]
                except:
                    z_month.append(np.nan)
                else:
                    z_month.append(ic)
            # z_year存的是一个period的heatmap
            z_year.append(z_month)
        # z存的是所有period的heatmap
        z.append(z_year)
    # 开始画图

    fig = make_subplots(rows=int(len(mean_monthly_ic.columns) / 3) + 1,
                        cols=3, subplot_titles=titles)
    count = 0
    for z1 in z:
        # z1 是其中一个subplot的z
        fig1 = ff.create_annotated_heatmap(x=x, y=y, z=np.array(z1),
                                           hoverinfo='z')
        # fig1.show()
        fig.add_trace(fig1.data[0], int(count / 3) + 1, count % 3 + 1)

        count += 1

    layout = dict()
    for i in range(1, count + 1):
        layout['xaxis' + str(i)] = {'type': 'category'}
        layout['yaxis' + str(i)] = {'type': 'category'}

    fig.update_layout(
        layout
    )

    return fig


def in_out_sample_factor_t_test(insample_factor: pd.Series, out_of_sample_factor: pd.Series):
    return stats.ttest_ind(insample_factor.values, out_of_sample_factor.values, nan_policy='omit')
