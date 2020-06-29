import numpy as np
import pandas as pd
from math import ceil
from scipy.stats import (
    norm as norm, linregress as linregress
)

pd.set_option('max_columns', None)
pd.set_option('max_rows', 300)


def first_last_trade_time(traded: pd.DataFrame, time_key='time_key'):
    """

    :param traded:
    :return:
    """
    time_list = traded[time_key].sort_values().values
    return time_list[0].astype(str), time_list[-1].astype(str)


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

    :param annualized_return:
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
    drawdown_percent = (drawdown / rolling_max)
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
                         dd.min(), clean_dd.min()))

        df = pd.DataFrame(data=data,
                          columns=('start', 'valley', 'end', 'days',
                                   'max drawdown',
                                   '99% max drawdown'))
        df['days'] = df['days'].astype(int)
        df['max drawdown'] = df['max drawdown'].astype(float)
        df['99% max drawdown'] = df['99% max drawdown'].astype(float)

        df['start'] = df['start'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['end'] = df['end'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['valley'] = df['valley'].dt.strftime('%Y-%m-%d %H:%M:%S')

        return df

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


def get_traded_pnl(traded: pd.DataFrame) -> pd.DataFrame:
    traded_ = traded.copy()  # type: pd.DataFrame
    traded_['cum_pos'] = traded_['dealt_qty'].cumsum()
    traded_['pair_id'] = np.where(traded_['cum_pos'] == 0, traded_.index, np.nan)
    traded_['pair_id'] = traded_['pair_id'].bfill()
    # traded_.set_index('order_time', inplace=True)
    traded_pnl = traded_.groupby('pair_id').agg({'cash_inflow': 'sum', 'order_time': 'last'})
    return traded_pnl


def win_rate(traded_pnl: pd.DataFrame, aggregate=None, compounded=True):
    """ calculates the win ratio for a period """
    return len(traded_pnl[traded_pnl['cash_inflow'] > 0]) / len(traded_pnl)


def avg_win(traded_pnl: pd.DataFrame):
    """
    calculates the average winning
    return/trade return for a period
    """
    return traded_pnl['cash_inflow'][traded_pnl['cash_inflow'] > 0].dropna().mean()


def avg_loss(traded_pnl: pd.DataFrame):
    """
    calculates the average low if
    return/trade return for a period
    """
    return traded_pnl['cash_inflow'][traded_pnl['cash_inflow'] < 0].dropna().mean()


def payoff_ratio(traded_pnl):
    """ measures the payoff ratio (average win/average loss) """
    return avg_win(traded_pnl) / abs(avg_loss(traded_pnl))


def kelly(traded_pnl):
    win_loss_ratio = payoff_ratio(traded_pnl)
    win_prob = win_rate(traded_pnl)
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
        confidence = confidence / 100

    return norm.ppf(1 - confidence, mu, sigma)



# related to benchmark backtesting metric


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
    # np.random.seed(0)
    # returns = np.random.randn(10000) / 100
    # returns[0] = 0
    # net_value = (1 + returns).cumprod()
    # net_value = pd.Series(net_value, index=pd.date_range(start='2020/01/01', periods=10000, freq='min'))
    # dd, ddp = drawdown(net_value)
    # ans = drawdown_details(dd)
    # print(ans)
    traded = pd.read_csv('traded_sample.csv')
    traded_pnl = get_traded_pnl(traded)
