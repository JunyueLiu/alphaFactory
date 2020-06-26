import math
import pandas as pd
import numpy as np

"""
detail definition see https://arxiv.org/pdf/1601.00991.pdf

"""


def rank(x: pd.Series) -> pd.Series:
    """
    rank(x) = cross-sectional rank

    :param x:
    :return:
    """
    assert isinstance(x.index, pd.MultiIndex)
    return x.groupby(level=0).rank(method='min', ascending=False)


def delay(x: pd.Series, d: int) -> pd.Series:
    """
    delay(x, d) = value of x d days ago
    :param x:
    :param d:
    :return:
    """
    assert d > 0
    return x.shift(d)


def correlation(x: pd.Series, y: pd.Series, d: int) -> pd.Series:
    """
    correlation(x, y, d) = time-serial correlation of x and y for the past d days

    :param x:
    :param y:
    :param d:
    :return:
    """
    return x.rolling(window=d).corr(y)


def covariance(x: pd.Series, y: pd.Series, d) -> pd.Series:
    """
    covariance(x, y, d) = time-serial covariance of x and y for the past d days
    :param x:
    :param y:
    :param d:
    :return:
    """
    return x.rolling(window=d).cov(y)


def scale(x: pd.Series, a: int = 1) -> pd.Series:
    """
    scale(x, a) = rescaled x such that sum(abs(x)) = a (the default is a = 1)
    :param x:
    :param a:
    :return:
    """
    # todo check this implementation is right
    return x.groupby(level=0).apply(lambda e: a * e / e.abs().sum())


def signedpower(x: pd.Series, a) -> pd.Series:
    """
    signedpower(x, a) = x^a
    :param x:
    :param a:
    :return:
    """
    # todo
    raise NotImplementedError
    pass


def decay_linear(x: pd.Series, d: int) -> pd.Series:
    """
    decay_linear(x, d) = weighted moving average over the past d days
    with linearly decaying weights d, d – 1, ..., 1 (rescaled to sum up to 1)
    :param x:
    :param d:
    :return:
    """
    # todo
    raise NotImplementedError
    pass


def indneutralize(x: pd.Series, g) -> pd.Series:
    """
    indneutralize(x, g) = x cross-sectionally neutralized against groups g (subindustries, industries, sectors, etc.),
    i.e., x is cross-sectionally demeaned within each group g

    :param x:
    :param g:
    :return:
    """
    pass


def ts_operation(x: pd.Series, d: int or float, operation) -> pd.Serie:
    """
    ts_{O}(x, d) = operator O applied across the time-series for the past d days;
    non-integer number of days d is converted to floor(d)
    :param x:
    :param d:
    :param operation:
    :return:
    """

    if isinstance(d, float):
        d = math.floor(d)
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(operation)
    else:
        return x.rolling(d).apply(operation)


def ts_min(x: pd.Series, d: int or float) -> pd.Serie:
    """
    ts_min(x, d) = time-series min over the past d days
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).min()
    else:
        return x.rolling(d).min()


def ts_max(x: pd.Series, d: int or float) -> pd.Serie:
    """
    ts_max(x, d) = time-series max over the past d days
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)
    return x.groupby(level=1).rolling(d).max()


def ts_argmax(x: pd.Series, d: int or float) -> pd.Serie:
    """
    ts_argmax(x, d) = which day ts_max(x, d) occurred on
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(lambda r: d - np.nanargmax(r))
    else:
        return x.rolling(d).apply(lambda r: d - np.nanargmax(r))


def ts_argmin(x: pd.Series, d: int or float) -> pd.Serie:
    """
    ts_argmin(x, d) = which day ts_min(x, d) occurred on
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(lambda r: d - np.nanargmin(r))
    else:
        return x.rolling(d).apply(lambda r: d - np.nanargmin(r))


def ts_rank(x: pd.Series, d: int or float) -> pd.Serie:
    """
    ts_rank(x, d) = time-series rank in the past d days
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)

    def func(a):
        return a.argsort().argsort()[-1] + 1

    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(func)
    else:
        return x.rolling(d).apply(func)


def min(x: pd.Series, d: int or float) -> pd.Serie:
    """
    min(x, d) = ts_min(x, d)

    :param x:
    :param d:
    :return:
    """
    return ts_min(x, d)


def max(x: pd.Series, d: int or float) -> pd.Serie:
    """
    max(x, d) = ts_max(x, d)
    :param x:
    :param d:
    :return:
    """
    return ts_max(x, d)


def sum(x: pd.Series, d: int or float) -> pd.Serie:
    """

    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)

    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).sum()
    else:
        return x.rolling(d).sum()


def product(x: pd.Series, d: int or float) -> pd.Serie:
    """
    product(x, d) = time-series product over the past d days
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)

    def func(x):
        return np.nancumprod(x)[-1]

    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(func)
    else:
        return x.rolling(d).apply(func)


def stddev(x: pd.Series, d: int or float) -> pd.Serie:
    """
    stddev(x, d) = moving time-series standard deviation over the past d days
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)

    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).std()
    else:
        return x.rolling(d).std()
