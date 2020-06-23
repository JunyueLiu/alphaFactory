import numpy as np
import pandas as pd
from math import ceil


def first_last_trade_time(traded: pd.DataFrame, time_key = 'time_key'):
    """

    :param traded:
    :return:
    """
    time_list = traded[time_key].sort_values().values
    return time_list[0], time_list[-1]


def compund_return(returns):
    """

    :param returns:
    :return:
    """
    return returns.add(1).prod() - 1


def deannualized(annualized_return, nperiods=252):
    """

    :param rf:
    :param nperiods:
    :return:
    """
    deannualized_return = np.power(1 + annualized_return, 1. / nperiods) - 1.
    return deannualized_return


def exposure(returns):
    """
    returns the market exposure time (returns != 0)
    """

    ex = len(returns[(~np.isnan(returns)) & (returns != 0)]) / len(returns)
    return ceil(ex * 100) / 100


def avg_return(returns, aggregate=None, compounded=True):
    """
    calculates the average return/trade return for a period
    returns = _utils._prepare_returns(returns)
    """
    if aggregate:
        returns = aggregate_returns(returns, aggregate, compounded)
    return returns[returns != 0].dropna().mean()


def sharpe_ratio(returns, rf=0., periods=252, annualize=True):
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
    """

    :param net_value:
    :param rf:
    :param compounded:
    :return:
    """
    years = (pd.to_datetime(net_value.index[-1]) - pd.to_datetime(net_value.index[0])).days / 365.

    res = abs(net_value[-1] - 1) ** (1.0 / years) - 1

    return res


def group_returns(returns, groupby, compounded):
    """

    :param returns:
    :param groupby:
    :param compounded:
    :return:
    """
    if compounded:
        return returns.groupby(groupby).apply(compund_return)
    return returns.groupby(groupby).sum()


def aggregate_returns(returns, period=None, compounded=True):
    """
    Aggregates returns based on date periods
    """

    if period is None:
        return returns

    if 'day' in period:
        return group_returns(returns, pd.Grouper(freq='D'), compounded=compounded)
    elif 'week' in period:
        return group_returns(returns, pd.Grouper(freq='W'), compounded=compounded)
    elif 'month' in period:
        return group_returns(returns, pd.Grouper(freq='M'), compounded=compounded)
    elif 'quarter' in period:
        return group_returns(returns, pd.Grouper(freq='Q'), compounded=compounded)
    elif "year" == period:
        return group_returns(returns, pd.Grouper(freq='Y'), compounded=compounded)
    elif not isinstance(period, str):
        return group_returns(returns, period, compounded)
    return returns


def drawdown(net_value: pd.Series):
    rolling_max = net_value.rolling(min_periods=1, window=len(net_value), center=False).max()
    drawdown = net_value - rolling_max
    drawdown_percent = (drawdown / rolling_max) * 100
    return drawdown, drawdown_percent


def best(returns, aggregate=None, compounded=True):
    """
    returns the best day/month/week/quarter/year's return
    """
    return aggregate_returns(returns, aggregate, compounded).max()


def worst(returns, aggregate=None, compounded=True):
    """
    returns the worst day/month/week/quarter/year's return
    """
    return aggregate_returns(returns, aggregate, compounded).min()


def win_rate(returns, aggregate=None, compounded=True):
    pass


def kelly():
    pass


def value_at_risk():
    pass


if __name__ == '__main__':
    traded = pd.read_csv('traded_group_sample.csv')
    start, end = first_last_trade_time(traded)
    print(start, end)
    df = pd.read_csv('sample_returns.csv')
    df['time_key'] = pd.to_datetime(df['time_key'])
    df.set_index('time_key', inplace=True)
    # compounded return
    print(compund_return(df['equity']))
    print(sharpe_ratio(df['equity'], 0.01, ))
    net_value = df['equity'].add(1).cumprod()
    dd, ddp = drawdown(net_value)
