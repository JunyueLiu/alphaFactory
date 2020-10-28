import jqdatasdk
import pandas as pd
from jqdatasdk import finance
from jqdatasdk import query
import os
import tqdm
import datetime
from alpha_research.factor_zoo.utils import get_nth_weekday_of_month, next_trading_date_dict

jqdatasdk.auth('17713571453', '')


def download_all_securities(types=[], date=None, data_folder='../local_data/joinquant'):
    # 'stock', 'fund', 'index', 'futures', 'options', 'etf', 'lof', 'fja', 'fjb', 'open_fund', 'bond_fund', 'stock_fund',
    # 'QDII_fund', 'money_market_fund', 'mixture_fund'
    name = 'stock'
    if len(types) > 0:
        name = ''.join([t + '_' for t in types])
        name = name[:-1]

    securities = jqdatasdk.get_all_securities(types=types, date=date)  # type: pd.DataFrame
    securities.to_csv(os.path.join(data_folder, name + '.csv'))


def download_balance_sheet(code, data_folder='../local_data/joinquant/balance_sheet'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    q = query(finance.STK_BALANCE_SHEET).filter(finance.STK_BALANCE_SHEET.code == code)
    df = finance.run_query(q)
    df.to_csv(os.path.join(data_folder, code + '.csv'))


def download_all_balance_sheet(code_list: list, data_folder='../local_data/joinquant/balance_sheet'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    for code in tqdm.tqdm(code_list):
        download_balance_sheet(code, data_folder=data_folder)


def download_income_statement(code, data_folder='../local_data/joinquant/income_statement'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    q = query(finance.STK_INCOME_STATEMENT).filter(finance.STK_INCOME_STATEMENT.code == code)
    df = finance.run_query(q)
    df.to_csv(os.path.join(data_folder, code + '.csv'))


def download_all_income_statement(code_list: list, data_folder='../local_data/joinquant/income_statement'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    for code in tqdm.tqdm(code_list):
        download_income_statement(code, data_folder=data_folder)


def download_cashflow_statement(code, data_folder='../local_data/joinquant/cashflow_statement'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    q = query(finance.STK_CASHFLOW_STATEMENT).filter(finance.STK_CASHFLOW_STATEMENT.code == code)
    df = finance.run_query(q)
    df.to_csv(os.path.join(data_folder, code + '.csv'))


def download_all_cashflow_statement(code_list: list, data_folder='../local_data/joinquant/cashflow_statement'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    for code in tqdm.tqdm(code_list):
        download_cashflow_statement(code, data_folder=data_folder)

def download_capital_change(code, data_folder='../local_data/joinquant/capital_change'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    q = query(finance.STK_CAPITAL_CHANGE).filter(finance.STK_CAPITAL_CHANGE.code == code)
    df = finance.run_query(q)
    df.to_csv(os.path.join(data_folder, code + '.csv'))


def download_all_capital_change(code_list: list, data_folder='../local_data/joinquant/capital_change'):
    if os.path.exists(data_folder) is False:
        os.makedirs(data_folder)
    for code in tqdm.tqdm(code_list):
        download_capital_change(code, data_folder=data_folder)


def concat_save_parquet(data_folder, save_path):
    df_list = []
    paths = os.listdir(data_folder)
    for path in tqdm.tqdm(paths):
        df = pd.read_csv(os.path.join(data_folder, path), index_col=0)
        df_list.append(df)
    print('Concat...')
    df = pd.concat(df_list, ignore_index=True)  # type: pd.DataFrame
    print('Save to parquet...')
    df.to_parquet(save_path, index=False)

def get_csi300_history_component(end_year, trading_date:list):
    # wrong
    # before 2014 the renew date is not the same with the rule now.
    start = '2005-04-08'
    # renew time:
    # 一般在每年 5 月和 11 月的下旬审核沪深 300 指数样本股，样本
    # 股调整实施时间分别是每年 6 月和 12 月的第二个星期五的下一交易
    # 日。

    # generate renew dates
    next_trading_date = next_trading_date_dict(trading_date)
    renew_datetimes = [start]
    today = datetime.datetime.now()
    for year in range(2005, end_year+1):
        for month in [6, 12]:
            date = get_nth_weekday_of_month(year, month, 4, 2)
            if date > today:
                continue
            next = next_trading_date[pd.to_datetime(date)].strftime('%Y-%m-%d')
            renew_datetimes.append(next)

    print(renew_datetimes)











if __name__ == '__main__':
    # df = pd.read_csv('../local_data/joinquant/stock.csv', index_col=0)
    # download_all_balance_sheet(df.index.to_list())
    # download_all_income_statement(df.index.to_list())
    # download_all_cashflow_statement(df.index.to_list())
    # download_all_capital_change(df.index.to_list())

    # concat_save_parquet('../local_data/joinquant/balance_sheet', '../local_data/joinquant/balance_sheet.parquet')
    # concat_save_parquet('../local_data/joinquant/income_statement', '../local_data/joinquant/income_statement.parquet')
    # concat_save_parquet('../local_data/joinquant/capital_change', '../local_data/joinquant/capital_change.parquet')

    td = '/Users/liujunyue/PycharmProjects/alphaFactory/local_data/joinquant/trading_date.csv'
    df = pd.read_csv(td, index_col=0, header=None)
    trading_list = pd.to_datetime(df[1].to_list())
    get_csi300_history_component(2020, trading_list)