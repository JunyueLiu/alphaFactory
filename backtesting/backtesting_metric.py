import numpy as np
import pandas as pd
from math import ceil
from scipy.stats import (
    norm as norm, linregress as linregress
)
pd.set_option('max_columns', None)
pd.set_option('max_rows', 300)


def first_last_trade_time(traded: pd.DataFrame, time_key = 'time_key'):
    """

    :param traded:
    :return:
    """
    time_list = traded[time_key].sort_values().values
    return time_list[0], time_list[-1]

def num_trade(traded: pd.DataFrame):
    return len(traded)

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

def remove_outliers(returns, quantile=.95):
    """ returns series of returns without the outliers """
    return returns[returns < returns.quantile(quantile)]

def drawdown_details(drawdown):
    """
    calculates drawdown details, including start/end/valley dates,
    duration, max drawdown and max dd for 99% of the dd period
    for every drawdown period
    """
    def _drawdown_details(drawdown):
        # mark no drawdown
        no_dd = drawdown == 0

        # extract dd start dates
        starts = ~no_dd & no_dd.shift(1)
        starts = list(starts[starts].index)

        # extract end dates
        ends = no_dd & (~no_dd).shift(1)
        ends = list(ends[ends].index)

        # no drawdown :)
        if not starts:
            return pd.DataFrame(
                index=[], columns=('start', 'valley', 'end', 'days',
                                   'max drawdown', '99% max drawdown'))

        # drawdown series begins in a drawdown
        if ends and starts[0] > ends[0]:
            starts.insert(0, drawdown.index[0])

        # series ends in a drawdown fill with last date
        if not ends or starts[-1] > ends[-1]:
            ends.append(drawdown.index[-1])

        # build dataframe from results
        data = []
        for i, _ in enumerate(starts):
            dd = drawdown[starts[i]:ends[i]]
            clean_dd = -remove_outliers(-dd, .99)
            data.append((starts[i], dd.idxmin(), ends[i],
                         (ends[i] - starts[i]).days,
                         dd.min() * 100, clean_dd.min() * 100))

        df = pd.DataFrame(data=data,
                           columns=('start', 'valley', 'end', 'days',
                                    'max drawdown',
                                    '99% max drawdown'))
        df['days'] = df['days'].astype(int)
        df['max drawdown'] = df['max drawdown'].astype(float)
        df['99% max drawdown'] = df['99% max drawdown'].astype(float)

        df['start'] = df['start'].dt.strftime('%Y-%m-%d %h:%M:%s')
        df['end'] = df['end'].dt.strftime('%Y-%m-%d %h:%M:%s')
        df['valley'] = df['valley'].dt.strftime('%Y-%m-%d %h:%M:%s')

        return df

    if isinstance(drawdown, pd.DataFrame):
        _dfs = {}
        for col in drawdown.columns:
            _dfs[col] = _drawdown_details(drawdown[col])
        return pd.concat(_dfs, axis=1)

    return _drawdown_details(drawdown)

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
    """ calculates the win ratio for a period """
    pass
def avg_win(returns):
    """
        calculates the average winning
        return/trade return for a period
        """
    pass

def avg_loss(returns, aggregate=None, compounded=True):
    """
    calculates the average low if
    return/trade return for a period
    """
    if aggregate:
        returns = aggregate_returns(returns, aggregate, compounded)
    return returns[returns < 0].dropna().mean()

def payoff_ratio(returns):
    """ measures the payoff ratio (average win/average loss) """
    return avg_win(returns) / abs(avg_loss(returns))

def kelly(returns):
    win_loss_ratio = payoff_ratio(returns)
    win_prob = win_rate(returns)
    lose_prob = 1 - win_prob

    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio


def value_at_risk(returns, sigma=1, confidence=0.95):
    """
    calculats the daily value-at-risk
    (variance-covariance calculation with confidence n)
    """
    mu = returns.mean()
    sigma *= returns.std()

    if confidence > 1:
        confidence = confidence/100

    return norm.ppf(1-confidence, mu, sigma)

if __name__ == '__main__':
    # traded = pd.read_csv('traded_group_sample.csv')
    # start, end = first_last_trade_time(traded)
    # print(start, end)
    # df = pd.read_csv('sample_returns.csv')
    # df['time_key'] = pd.to_datetime(df['time_key'])
    # df.set_index('time_key', inplace=True)
    # # compounded return
    # print(compund_return(df['equity']))
    # print(sharpe_ratio(df['equity'], 0.01, ))
    # net_value = df['equity'].add(1).cumprod()
    np.random.seed(0)
    returns = np.random.randn(10000) / 100
    returns[0] = 0
    net_value = (1 + returns).cumprod()
    net_value = pd.Series(net_value, index=pd.date_range(start='2020/01/01', periods=10000, freq='min'))
    dd, ddp = drawdown(net_value)
    ans = drawdown_details(dd)
    print(ans)
