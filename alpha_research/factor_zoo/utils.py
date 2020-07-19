import math
import pandas as pd
import numpy as np

"""
detail definition see https://arxiv.org/pdf/1601.00991.pdf

"""


def returns(close: pd.Series) -> pd.Series:
    """
    returns = daily close-to-close returns
    :param close:
    :return:
    """
    if isinstance(close.index, pd.MultiIndex):
        return close.groupby(level=1).pct_change(1)
    else:
        return close.pct_change(1)


def vwap(prices: pd.Series, volume: pd.Series) -> pd.Series:
    """
    df['vwap'] = (np.cumsum(df.quantity * df.price) / np.cumsum(df.quantity))
    vwap = daily volume-weighted average price
    :param prices:
    :param volume:
    :return:
    """
    if isinstance(prices.index, pd.MultiIndex):
        return (volume * prices).groupby(level=1).cumsum() / volume.groupby(level=1).cumsum()
    else:
        return (volume * prices).cumsum() / volume.cumsum()


def adv(prices: pd.Series, volume, d: int) -> pd.Series:
    """
    adv{d} = average daily dollar volume for the past d days
    :param d:
    :param volume:
    :return:
    """
    if isinstance(prices.index, pd.MultiIndex):
        return (prices * volume).groupby(level=1).rolling(d).mean()
    else:
        return (prices * volume).rolling(d).mean()


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
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).shift(d)
    else:
        return x.shift(d)


def correlation(x: pd.Series, y: pd.Series, d: int) -> pd.Series:
    """
    correlation(x, y, d) = time-serial correlation of x and y for the past d days

    :param x:
    :param y:
    :param d:
    :return:
    """
    # todo multiindex
    if isinstance(x.index, pd.MultiIndex):
        x.name = 'x'
        y.name = 'y'
        j = x.to_frame().join(y.to_frame())
        res = []

        for g in j.groupby(level=1):

            a = g[1][x.name]
            b = g[1][y.name]
            r = a.rolling(window=d).corr(b)
            res.append(r)
        return pd.concat(res)
    else:
        return x.rolling(window=d).corr(y)


def covariance(x: pd.Series, y: pd.Series, d) -> pd.Series:
    """
    covariance(x, y, d) = time-serial covariance of x and y for the past d days
    :param x:
    :param y:
    :param d:
    :return:
    """
    # todo multiindex
    if isinstance(x.index, pd.MultiIndex):
        j = x.to_frame().join(y.to_frame())
        res = []
        for g in j.groupby(level=1):
            a = g[1][x.name]
            b = g[1][y.name]
            r = a.rolling(window=d).cov(b)
            res.append(r)
        return pd.concat(res)
    else:
        return x.rolling(window=d).cov(y)

def delta(x: pd.Series, d: int) -> pd.Series:
    """

    :param x:
    :param d:
    :return:
    """
    assert d > 0
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).diff(d)
    else:
        return x - x.shift(d)

def scale(x: pd.Series, a: int = 1) -> pd.Series:
    """
    scale(x, a) = rescaled x such that sum(abs(x)) = a (the default is a = 1)
    :param x:
    :param a:
    :return:
    """
    # todo check this implementation is right
    assert isinstance(x.index, pd.MultiIndex)
    return x.groupby(level=0).apply(lambda e: a * e / e.abs().sum())


def signedpower(x: pd.Series, a) -> pd.Series:
    """
    signedpower(x, a) = x^a
    :param x:
    :param a:
    :return:
    """
    return x.pow(a)


def decay_linear(x: pd.Series, d: int) -> pd.Series:
    """
    decay_linear(x, d) = weighted moving average over the past d days
    with linearly decaying weights d, d – 1, ..., 1 (rescaled to sum up to 1)
    :param x:
    :param d:
    :return:
    """
    # todo https://www.joinquant.com/community/post/detailMobile?postId=10674&page=&limit=20&replyId=&tag=
    if isinstance(d, float):
        d = math.floor(d)

    def func(a):
        weights = np.arange(1, d + 1)
        weights = weights / weights.sum()
        return np.nansum(weights * a)

    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(func)
    else:
        return x.rolling(d).apply(func)


def indneutralize(x: pd.Series, g) -> pd.Series:
    """
    indneutralize(x, g) = x cross-sectionally neutralized against groups g (subindustries, industries, sectors, etc.),
    i.e., x is cross-sectionally demeaned within each group g

    :param x:
    :param g:
    :return:
    """
    if x.index.nlevels != 3:
        raise ValueError(
            'x has not grouped by industry. Expect 3 levels of index, but {} given instead.'.format(x.index.nlevels))
    # todo check this is right.
    return x.groupby(level=[0, 2]).apply(lambda a: a - a.mean())


def ts_operation(x: pd.Series, d: int or float, operation) -> pd.Series:
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


def ts_min(x: pd.Series, d: int or float) -> pd.Series:
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


def ts_max(x: pd.Series, d: int or float) -> pd.Series:
    """
    ts_max(x, d) = time-series max over the past d days
    :param x:
    :param d:
    :return:
    """
    if isinstance(d, float):
        d = math.floor(d)
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).max()
    else:
        return x.rolling(d).max()


def ts_argmax(x: pd.Series, d: int or float) -> pd.Series:
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


def ts_argmin(x: pd.Series, d: int or float) -> pd.Series:
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


def ts_rank(x: pd.Series, d: int or float) -> pd.Series:
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


def min(x: pd.Series, d: int or float) -> pd.Series:
    """
    min(x, d) = ts_min(x, d)

    :param x:
    :param d:
    :return:
    """
    return ts_min(x, d)


def max(x: pd.Series, d: int or float) -> pd.Series:
    """
    max(x, d) = ts_max(x, d)
    :param x:
    :param d:
    :return:
    """
    return ts_max(x, d)


def sum(x: pd.Series, d: int or float) -> pd.Series:
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


def product(x: pd.Series, d: int or float) -> pd.Series:
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


def stddev(x: pd.Series, d: int or float) -> pd.Series:
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
