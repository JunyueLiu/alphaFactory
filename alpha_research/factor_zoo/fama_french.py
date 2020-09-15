import pandas as pd
import numpy as np
import os
import json

from alpha_research.factor_zoo.utils import load_jointquant_fundamental, load_ret_parquet, next_trading_date_dict, \
    no_trading_date_to_next, combine_market_with_fundamental, returns, combine_fundamental_with_fundamental


def small_minus_big_groupby_function(df: pd.DataFrame, col: str, q: float, long: bool, short: bool):
    tmp = pd.DataFrame()
    if long:
        small = df[df[col] <= df[col].quantile(q)]
        tmp = tmp.append(small)

    if short:
        big = df[df[col] >= df[col].quantile(1 - q)]
        big['ret'] = - big['ret']
        tmp = tmp.append(big)
    return np.average(tmp['ret'], weights=tmp['weight'])


def high_minus_low_groupby_function(df: pd.DataFrame, col: str, q: float, long: bool, short: bool):
    tmp = pd.DataFrame()
    if long:
        high = df[df[col] >= df[col].quantile(1 - q)]
        tmp = tmp.append(high)

    if short:
        low = df[df[col] <= df[col].quantile(q)]
        low['ret'] = - low['ret']
        tmp = tmp.append(low)
    return np.average(tmp['ret'], weights=tmp['weight'])


def smb(market_data: pd.DataFrame or pd.Series,
        total_shares: pd.Series,
        start=None, end=None,
        trading_date: None or list = None,
        suspend_data: None or pd.Series = None,
        universe: pd.Series or pd.DataFrame = None,
        long: bool = True,
        short: bool = True,
        quantile: float = 0.2,
        weight: pd.Series or str = 'cap'
        ) -> pd.DataFrame:
    total_shares_name = total_shares.name
    merge_df = combine_market_with_fundamental(market_data, total_shares, start, end, trading_date, suspend_data,
                                               universe)
    if 'ret' not in merge_df.columns:
        merge_df['ret'] = returns(merge_df['close'])
    merge_df['total_capital'] = merge_df['close'] * merge_df[total_shares_name]
    merge_df = merge_df[['ret', 'total_capital']]
    if isinstance(weight, pd.Series):
        weight.name = 'weight'
        merge_df = merge_df.join(weight)
    elif isinstance(weight, str):
        if weight == 'cap':
            merge_df['weight'] = merge_df['total_capital']
        elif weight == 'equal':
            merge_df['weight'] = 1
    merge_df.dropna(inplace=True)
    factor = merge_df.groupby(level=0).apply(
        lambda x: small_minus_big_groupby_function(x, 'total_capital', quantile, long, short))
    factor.name = 'SMB'
    return factor.to_frame()


def hml(market_data: pd.DataFrame or pd.Series,
        net_book: pd.Series,
        total_shares: pd.Series,
        start=None, end=None,
        trading_date: None or list = None,
        suspend_data: None or pd.Series = None,
        universe: pd.Series or pd.DataFrame = None,
        long: bool = True,
        short: bool = True,
        quantile: float = 0.2,
        weight: pd.Series or str = 'cap'):
    total_shares_name = total_shares.name
    net_book_name = net_book.name
    facotrs = combine_fundamental_with_fundamental(net_book, total_shares, start,
                                                   end, universe)

    merge_df = combine_market_with_fundamental(market_data, facotrs, start, end, trading_date, suspend_data,
                                               universe)
    if 'ret' not in merge_df.columns:
        merge_df['ret'] = returns(merge_df['close'])
    merge_df['total_capital'] = merge_df['close'] * merge_df[total_shares_name]
    merge_df = merge_df[['ret', 'total_capital', net_book_name]]
    if isinstance(weight, pd.Series):
        weight.name = 'weight'
        merge_df = merge_df.join(weight)
    elif isinstance(weight, str):
        if weight == 'cap':
            merge_df['weight'] = merge_df['total_capital']
        elif weight == 'equal':
            merge_df['weight'] = 1
    merge_df['market_to_book'] = merge_df['total_capital'] / merge_df[net_book_name]
    merge_df.dropna(inplace=True)
    factor = merge_df.groupby(level=0).apply(
        lambda x: high_minus_low_groupby_function(x, 'market_to_book', quantile, long, short))
    factor.name = 'HML'
    return factor.to_frame()

if __name__ == '__main__':
    # raw_factor
    path = r'../../local_data/joinquant/capital_change.parquet'
    df = load_jointquant_fundamental(path)
    fundamental_data2 = load_jointquant_fundamental(r'../../local_data/joinquant/balance_sheet.parquet')
    # return data
    # ret = load_ret_parquet(r'../../local_data/A_Shares.parquet')
    market_data = pd.read_parquet(r'../../local_data/A_Shares.parquet')
    # universe
    universe = pd.read_parquet(r'csi300.parquet')
    # trading_date
    td = '../../local_data/joinquant/trading_date.csv'
    trading_date = pd.read_csv(td, index_col=0, header=None)
    trading_date = pd.to_datetime(trading_date[1].to_list())

    start = '2019-01-01'
    end = '2020-01-01'
    total_shares = df['share_total']
    net_book = fundamental_data2['total_owner_equities']
    # merge_df = combine_market_fundamental(market_data, total_shares, start, end, trading_date, universe=universe)
    #
    # total_shares_name = total_shares.name
    # if 'ret' not in merge_df.columns:
    #     merge_df['ret'] = returns(merge_df['close'])
    # merge_df['total_capital'] = merge_df['close'] * merge_df[total_shares_name]
    # merge_df.dropna(inplace=True)
    smb_factor = smb(market_data, total_shares, start, end, trading_date, universe=universe)
    hml_factor = hml(market_data, net_book, total_shares, start, end, trading_date, universe=universe)