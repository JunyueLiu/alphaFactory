import yfinance as yf
import os


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
    download_kline_and_save('^HSI', 'r../local_data')
