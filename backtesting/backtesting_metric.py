import numpy as np
import pandas as pd
from math import ceil


def deannualized(annualized_return, nperiods=252):
    """

    :param rf:
    :param nperiods:
    :return:
    """
    deannualized_return = np.power(1 + annualized_return, 1. / nperiods) - 1.
    return deannualized_return


def sharpe(returns, rf=0., periods=252, annualize=True):
    """

    :param returns:
    :param rf:
    :param periods:
    :param annualize:
    :return:
    """
    if rf != 0 and periods is None:
        raise Exception('Must provide periods if rf != 0')

    rf = deannualized(rf, periods)
    res = (returns.mean() - rf) / returns.std()

    if annualize:
        return res * np.sqrt(1 if periods is None else periods)
    return res


def sortino(returns, rf=0, periods=252, annualize=True):
    """

    https://www.investopedia.com/terms/s/sortinoratio.asp

    """

    if rf != 0 and periods is None:
        raise Exception('Must provide periods if rf != 0')

    downside = (returns[returns < 0] ** 2).sum() / len(returns)
    res = returns.mean() / np.sqrt(downside)

    if annualize:
        return res * np.sqrt(1 if periods is None else periods)

    return res


def cagr(net_value, rf=0., compounded=True):
    years = (net_value.index[-1] - net_value.index[0]).days / 365.

    res = abs(net_value[-1] - 1) ** (1.0 / years) - 1

    return res


def exposure(returns):
    """
    returns the market exposure time (returns != 0)
    """

    def _exposure(ret):
        ex = len(ret[(~np.isnan(ret)) & (ret != 0)]) / len(ret)
        return ceil(ex * 100) / 100

    if isinstance(returns, pd.DataFrame):
        _df = {}
        for col in returns.columns:
            _df[col] = _exposure(returns[col])
        return pd.Series(_df)
    return _exposure(returns)


def win_rate(returns, aggregate=None, compounded=True):
    pass


def drawdown(net_value: pd.Series):
    rolling_max = net_value.rolling(min_periods=1, window=len(net_value), center=False).max()
    drawdown = net_value - rolling_max
    drawdown_percent = (drawdown / rolling_max) * 100
    return drawdown, drawdown_percent

if __name__ == '__main__':
    df = pd.read_csv('sample_returns.csv')
    df.set_index('time_key', inplace=True)
    net_value = df['equity'].add(1).cumprod()
    dd, ddp = drawdown(net_value)
