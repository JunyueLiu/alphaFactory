import yfinance as yf
import os
import threading
import pandas as pd
import time

from data_downloader.multi_asset_data_merger import merge_single_asset
from data_downloader.utils import joinquant_to_yfinance_ticker


def download_kline_and_save(code, save_folder=''):
    ticker = yf.Ticker(code)
    data = ticker.history(period='max', )
    start = str(data.index[0])
    end = str(data.index[-1])
    data.columns = [c.lower() for c in data.columns]
    data['code'] = code
    file_name = '{}_{}_{}.csv'.format(code, start, end)
    data.to_csv(os.path.join(save_folder, file_name))
    print('save:', file_name)


def multi_thread_download(code_list: list, save_folder=''):
    threads = []
    for code in code_list:
        threads.append(threading.Thread(target=download_kline_and_save, args=(code, save_folder)))
        try:
            threads[-1].start()
            time.sleep(0.2)
        except:
            pass

    for i in range(len(threads)):
        threads[i].join()

    print("Done.")

def merge_data_save_parquet(paths, save_path,time_key='Date', code_key = 'code'):
    df = merge_single_asset(paths, time_key=time_key, code_key=code_key) # type:pd.DataFrame
    print('Save...')
    df.to_parquet(save_path)


if __name__ == '__main__':
    # hsi_component = ['0001.HK', '0002.HK', '0003.HK', '0005.HK', '0006.HK',
    #                  '0011.HK', '0012.HK', '0016.HK', '0017.HK', '0019.HK',
    #                  '0027.HK', '0066.HK', '0083.HK', '0101.HK', '0151.HK',
    #                  '0175.HK', '0267.HK', '0288.HK', '0386.HK', '0388.HK',
    #                  '0669.HK', '0688.HK', '0700.HK', '0762.HK', '0823.HK',
    #                  '0857.HK', '0883.HK', '0939.HK', '0941.HK', '1038.HK',
    #                  '1044.HK', '1088.HK', '1093.HK', '1109.HK', '1113.HK',
    #                  '1177.HK', '1299.HK', '1398.HK', '1928.HK', '1997.HK',
    #                  '2007.HK', '2018.HK', '2313.HK', '2318.HK', '2319.HK',
    #                  '2382.HK', '2388.HK', '2628.HK', '3328.HK', '3988.HK']
    # for c in hsi_component:
    #     download_kline_and_save(c, '/Users/liujunyue/PycharmProjects/alphaFactory/local_data')
    # download_kline_and_save('^HSI', 'r../local_data')
    # df = pd.read_csv('../local_data/joinquant/stock.csv', index_col=0)
    # code_list = joinquant_to_yfinance_ticker(df.index.to_list())
    # multi_thread_download(code_list, r'../local_data/CHINA')
    files = os.listdir(r'../local_data/CHINA')
    paths = [os.path.join(r'../local_data/CHINA', f) for f in files]
    merge_data_save_parquet(paths, r'../local_data/A_Shares.parquet')