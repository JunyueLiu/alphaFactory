import yfinance as yf
import os

def download_kline_and_save(code, save_folder=''):
    ticker = yf.Ticker(code)
    data = ticker.history(period='10y',)
    start = str(data.index[0])
    end = str(data.index[-1])
    data['code'] = code
    file_name = '{}_{}_{}.csv'.format(code, start, end)
    data.to_csv(os.path.join(save_folder, file_name))
    print('save:', file_name)

if __name__ == '__main__':
    hsi_component = ['0001.HK', '0011.HK', '1398.HK', '2318.HK','1299.HK','1928.HK', '0027.HK']
    for c in hsi_component:
        download_kline_and_save(c, '/Users/liujunyue/PycharmProjects/alphaFactory/local_data')