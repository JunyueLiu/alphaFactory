import pandas as pd
import numpy as np
import os
import json

from alpha_research.factor_zoo.utils import load_jointquant_fundamental, load_ret_parquet, next_trading_date_dict, \
    no_trading_date_to_next, combine_market_fundamental, returns


def smb(market_data: pd.DataFrame or pd.Series,
        total_shares: pd.Series,
        start=None, end=None,
        trading_date: None or list = None,
        suspend_data: None or pd.Series = None,
        universe: pd.Series or pd.DataFrame = None,
        long_short: bool = True,
        quantile: float = 0.2,
        weight=''
        ) -> pd.DataFrame:
    total_shares_name = total_shares.name
    merge_df = combine_market_fundamental(market_data, total_shares, start, end, trading_date, suspend_data, universe)
    if 'ret' not in merge_df.columns:
        merge_df['ret'] = returns(merge_df['close'])
    merge_df['total_capital'] = merge_df['close'] * merge_df[total_shares_name]
    merge_df.dropna(inplace=True)
    merge_df


def hml():
    pass




if __name__ == '__main__':
    # raw_factor
    path = r'../../local_data/joinquant/capital_change.parquet'
    df = load_jointquant_fundamental(path)
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
    merge_df = combine_market_fundamental(market_data, total_shares, start, end, trading_date, universe=universe)

    total_shares_name = total_shares.name
    if 'ret' not in merge_df.columns:
        merge_df['ret'] = returns(merge_df['close'])
    merge_df['total_capital'] = merge_df['close'] * merge_df[total_shares_name]
    merge_df.dropna(inplace=True)
