import os
import json
import datetime
import math
import pandas as pd
import numpy as np
import tqdm

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
        return (prices * volume).groupby(level=1).rolling(d).mean().droplevel(0).sort_index()
    else:
        return (prices * volume).rolling(d).mean()

def abs(x:pd.Series) -> pd.Series:
    return x.abs()


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
    if isinstance(d, float):
        d = math.floor(d)
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
        return pd.concat(res).sort_index()
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
        return pd.concat(res).sort_index()
    else:
        return x.rolling(window=d).cov(y)


def delta(x: pd.Series, d: int) -> pd.Series:
    """

    :param x:
    :param d:
    :return:
    """
    assert d > 0
    if isinstance(d, float):
        d = math.floor(d)
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
        return x.groupby(level=1).rolling(d).apply(func).droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).min().droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).max().droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).apply(lambda r: d - np.nanargmax(r)).droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).apply(lambda r: d - np.nanargmin(r)).droplevel(0).sort_index()
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
        # 这里sort两次是啥意思？
        # https://stackoverflow.com/questions/14440187/rank-data-over-a-rolling-window-in-pandas-dataframe
        # x = np.array([3, 1, 2])
        # x.argsort()
        # Out[5]: array([1, 2, 0])
        # x.argsort().argsort()
        # Out[6]: array([2, 0, 1])
        return a.size - a.argsort().argsort()[-1]
    if isinstance(x.index, pd.MultiIndex):
        return x.groupby(level=1).rolling(d).apply(func).droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).sum().droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).apply(func).droplevel(0).sort_index()
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
        return x.groupby(level=1).rolling(d).std().droplevel(0).sort_index()
    else:
        return x.rolling(d).std()


"""

relative to fundamental

"""


def load_csmar_data(path: str):
    df = pd.read_csv(path, sep='\t', encoding='gbk', header=[0, 1, 2], dtype={0: str}, infer_datetime_format=True)
    df.columns = df.columns.droplevel([1, 2])

    return df


def get_csmar_code_chinese(field: str, data_folder='../../local_data/fundamental'):
    simple = {
        "Stkcd": "股票代码",
        "Accper": "会计期间",
        "Typrep": "报表类型",
        "DataSources": "公告来源",
        "SubjectCode": "科目编码",
        "SubjectName": "科目名称",
    }
    if field in simple:
        return simple[field]

    tables = {
        "A": 'balance_sheet/csmar_balance_sheet_code.json',
        'B': 'income_statement/csmar_income_statement_code.json',
        'C': 'cashflow/direct/csmar_cashflow_dir_code.json',
        'D': 'cashflow/indirect/csmar_cashflow_ind_code.json',
        'F': 'equity/csmar_equity_code.json'
    }
    json_path = tables[field[0]]

    with open(os.path.join(data_folder, json_path)) as f:
        codes = json.load(f)

    return codes.get(field, None)


def load_jointquant_fundamental(path: str):
    df = pd.read_parquet(path)
    df['code'] = df['code'].apply(lambda x: x.split('.')[0])
    df['pub_date'] = pd.to_datetime(df['pub_date'])
    df.set_index(['pub_date', 'code'], inplace=True)
    df.sort_index(inplace=True)
    return df


def load_ret_parquet(path: str) -> pd.Series:
    df = pd.read_parquet(path)
    ret = returns(df['close'])
    return ret


def next_trading_date_dict(trading_date: list):
    start = trading_date[0]
    end = trading_date[-1]
    date = pd.date_range(start, end=end, freq='D')
    normal_date = pd.DataFrame(index=date)
    trading_date_df = pd.DataFrame(trading_date, index=trading_date, columns=['next_trading_date'])
    next_trading_date = normal_date.join(trading_date_df).fillna(method='bfill').shift(-1).to_dict()[
        'next_trading_date']  # type: dict
    return next_trading_date


def no_trading_date_to_next(date, trading_date: list, next_trading_date: dict):
    if date in trading_date:
        return date
    else:
        return next_trading_date[date]


def get_nth_weekday_of_month(year: int, month: int, weekday: int, n: int):
    """
    Answer the question like what is the date of the first Monthday in May 2020.
    :param year: int
    :param month: int
    :param weekday: int (0-6)
    :param n:
    :return:
    """
    first_day = datetime.datetime(year, month, 1)
    first_day_weekday = first_day.weekday()
    day_count = weekday - first_day_weekday
    if day_count < 0:
        day_count += 7
    day_count += (n - 1) * 7
    return first_day + datetime.timedelta(days=day_count)


def component_to_universe(component_df: pd.DataFrame, start=None, end=None, trading_date: None or list = None,
                          universe_name='universe'):
    """
    component_df：
    code,in_time,out_time
    000001,2005-04-08,
    000002,2005-04-08,
    000008,2016-12-12,2018-06-11

    date,code,universe
    2010-01-04,000001,True
    2010-01-04,000002,True
    2010-01-04,000009,True
    2010-01-04,000012,True
    2010-01-04,000021,True
    2010-01-04,000024,True
    2010-01-04,000027,True
    2010-01-04,000031,True

    :param component_df:
    :param start:
    :param end:
    :param trading_date:
    :param universe_name:
    :return:
    """
    component_df.fillna(pd.to_datetime(datetime.datetime.now()).strftime('%Y-%m-%d'), inplace=True)
    if start is None:
        start = component_df['in_time'].min()
    if end is None:
        end = component_df['out_time'].max()
    if isinstance(start, pd.Timestamp) is False:
        start = pd.to_datetime(start)
    if isinstance(end, pd.Timestamp) is False:
        end = pd.to_datetime(end)

    # date_index = pd.date_range(start, end, freq='D')

    # pd.MultiIndex.from_product((date_index, component_df.index))

    # slow...
    #

    universe = pd.DataFrame()

    for idx, row in tqdm.tqdm(component_df.iterrows()):
        index = pd.date_range(row['in_time'], row['out_time'], freq='D')
        index.name = 'date'
        df = pd.DataFrame(index=index)
        df['code'] = row.name
        universe = universe.append(df)
    universe = universe.sort_index()
    universe = universe.loc[start: end]
    if trading_date is not None:
        trade = pd.DataFrame(index=trading_date)
        universe = trade.join(universe).dropna()
        universe.index.name = 'date'

    universe[universe_name] = True
    universe = universe.reset_index().set_index(['date', 'code']).sort_index()
    return universe


def get_latest_info_by_date(df: pd.DataFrame, start_pd: pd.Timestamp):
    """

    :param df:
    :param start_pd:
    :return:
    """
    names = df.index.names
    df = df.sort_index(level=[1, 0]).reset_index()
    df[names[0]] = df[names[0]].apply(
        lambda x: x if x > start_pd else start_pd)
    df = df.drop_duplicates(subset=names, keep='last')
    return df.set_index(names).sort_index()


def combine_market_with_fundamental(market_data: pd.DataFrame or pd.Series,
                                    fundamental_data: pd.DataFrame or pd.Series,
                                    start=None, end=None,
                                    trading_date: None or list = None,
                                    suspend_data: None or pd.Series = None,
                                    universe: pd.Series or pd.DataFrame = None,
                                    ) -> pd.DataFrame:
    assert isinstance(market_data.index, pd.MultiIndex)
    assert isinstance(fundamental_data.index, pd.MultiIndex)
    if isinstance(fundamental_data, pd.Series):
        fundamental_data = fundamental_data.to_frame()

    if isinstance(market_data, pd.Series):
        market_data = market_data.to_frame()

    names = fundamental_data.index.names
    if start is not None:
        start_pd = pd.to_datetime(start)

        market_data = market_data.loc[start_pd:]

        # transform the fundamental_data that contains data it should have know at the start date
        fundamental_data = get_latest_info_by_date(fundamental_data, start_pd)
        if universe is not None:
            universe = universe.loc[start_pd:]

    if end is not None:
        end_pd = pd.to_datetime(end)
        market_data = market_data.loc[:end_pd]
        fundamental_data = fundamental_data.loc[:end_pd]
        if universe is not None:
            universe = universe.loc[:end_pd]

    # filter out the universe if necessary
    #       date,code,universe
    #     2010-01-04,000001,True
    #     2010-01-04,000002,True
    #     2010-01-04,000009,True
    #     2010-01-04,000012,True
    #     2010-01-04,000021,True
    #     2010-01-04,000024,True
    #     2010-01-04,000027,True
    #     2010-01-04,000031,True
    if universe is not None:
        market_data = market_data.loc[universe.index, :]
        fundamental_data = fundamental_data.loc[(slice(None), universe.index.get_level_values(1).unique()), :]

    if suspend_data is not None:
        market_data = market_data.loc[suspend_data.index, :]

    # change announcement date to trading date if necessary
    if trading_date is not None:
        fundamental_data = fundamental_data.reset_index()
        next_trading_dict = next_trading_date_dict(trading_date)
        fundamental_data[names[0]] = fundamental_data[names[0]].apply(
            lambda x: no_trading_date_to_next(x, trading_date, next_trading_dict))
        fundamental_data = fundamental_data.set_index(names)

    # join the data
    fundamental_data.index.names = market_data.index.names

    merge_df = market_data.join(fundamental_data)
    ## this is to make sure no future information is in the joined df
    merge_df = merge_df.groupby(level=1).fillna(method='ffill')
    ## if the raw_factor data is not included the data, could be nan
    return merge_df


def combine_fundamental_with_fundamental(fundamental_data1: pd.DataFrame or pd.Series,
                                         fundamental_data2: pd.DataFrame or pd.Series,
                                         start=None, end=None,
                                         universe: pd.Series or pd.DataFrame = None,
                                         ) -> pd.DataFrame:
    assert isinstance(fundamental_data1.index, pd.MultiIndex)
    assert isinstance(fundamental_data2.index, pd.MultiIndex)
    if isinstance(fundamental_data1, pd.Series):
        fundamental_data1 = fundamental_data1.to_frame()

    if isinstance(fundamental_data2, pd.Series):
        fundamental_data2 = fundamental_data2.to_frame()

    if start is not None:
        start_pd = pd.to_datetime(start)

        # transform the fundamental_data that contains data it should have know at the start date

        fundamental_data1 = get_latest_info_by_date(fundamental_data1, start_pd)
        fundamental_data2 = get_latest_info_by_date(fundamental_data2, start_pd)
        if universe is not None:
            universe = universe.loc[start_pd:]

    if end is not None:
        end_pd = pd.to_datetime(end)
        fundamental_data1 = fundamental_data1.loc[:end_pd]
        fundamental_data2 = fundamental_data2.loc[:end_pd]
        if universe is not None:
            universe = universe.loc[:end_pd]

    if universe is not None:
        fundamental_data1 = fundamental_data1.loc[(slice(None), universe.index.get_level_values(1).unique()), :]
        fundamental_data2 = fundamental_data2.loc[(slice(None), universe.index.get_level_values(1).unique()), :]

    merge_df = fundamental_data1.join(fundamental_data2, how='outer', lsuffix='l_')
    merge_df = merge_df.groupby(level=1).fillna(method='ffill')
    return merge_df




def filter_suspend(ret, suspend: dict):
    pass


if __name__ == '__main__':
    # td = '/Users/liujunyue/PycharmProjects/alphaFactory/local_data/joinquant/trading_date.csv'
    # df = pd.read_csv(td, index_col=0, header=None)
    # trading_list = pd.to_datetime(df[1].to_list())
    # capital_change = load_jointquant_fundamental(
    #     '/Users/liujunyue/PycharmProjects/alphaFactory/local_data/joinquant/capital_change.parquet')
    # next_trading_date_dict(trading_list)
    # print(get_nth_weekday_of_month(2020, 4, 0, 1))
    # component_df = pd.read_parquet(r'../../local_data/CHINA/csi300_component.parquet')
    # u = component_to_universe(component_df, '2010-01-01', trading_date=trading_list)

    universe = pd.read_parquet(r'csi300.parquet')
    fundamental_data1 = load_jointquant_fundamental(r'../../local_data/joinquant/capital_change.parquet')
    fundamental_data2 = load_jointquant_fundamental(r'../../local_data/joinquant/balance_sheet.parquet')
    start = '2019-01-01'
    end = '2020-01-01'
    start_pd = pd.to_datetime(start)

    # transform the fundamental_data that contains data it should have know at the start date

    # fundamental_data1 = get_latest_info_by_date(fundamental_data1, start_pd)
    # fundamental_data2 = get_latest_info_by_date(fundamental_data2, start_pd)
    merged = combine_fundamental_with_fundamental(fundamental_data1.share_total, fundamental_data2.total_owner_equities,start, end, universe)
