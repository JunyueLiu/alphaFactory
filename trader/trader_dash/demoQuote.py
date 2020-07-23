from gateway.quote_base import QuoteBase
import yfinance as yf
import pandas as pd
import threading

import time


class DemoQuote(QuoteBase):

    def __init__(self):
        super().__init__()
        tickers = ['^HSI']
        self.data = pd.DataFrame()
        for code in tickers:
            ticker = yf.Ticker(code)
            data = ticker.history(period='7d', interval='1m')
            data['code'] = code
            data['sub_type'] = "K_1M"
            data.columns = [c.lower() for c in data.columns]
            self.data = self.data.append(data)
        self.data.index = self.data.index.tz_localize(None)
        self.data.reset_index(inplace=True)
        self.data.set_index(['Datetime', 'code'], inplace=True)
        self.time_ = self.data.index.get_level_values(0).unique().to_list()
        self.cur_data = None

        quote = self

        class myThread(threading.Thread):  # 继承父类threading.Thread
            def __init__(self):
                threading.Thread.__init__(self)
                self.time_list = None
                self.count = 100
                self.time = None

            def run(self):

                self.time_list = quote.time_
                while self.count < len(self.time_list):
                    self.time = self.time_list[:self.count]
                    self.count += 1
                    # print(self.count)
                    quote.cur_data = quote.data.loc[(self.time, slice(None)), :].sort_index(ascending=True)
                    time.sleep(3)
                    # print(quote.cur_data)

        my_thred = myThread()
        my_thred.start()

    def subscribe(self, code_list, subtype_list, *args, **kwargs):
        for code in code_list:
            ticker = yf.Ticker(code)
            for subtype in subtype_list:
                # "K_1M", "K_3M", "K_5M", "K_15M",
                # "K_30M", "K_60M", "K_DAY", "K_WEEK",
                # "K_MON", "K_QUARTER", "K_YEAR"
                if subtype == "K_1M":
                    data = ticker.history(period='7d', interval='1m')
                elif subtype == "K_5M":
                    data = ticker.history(period='7d', interval='5m')
                elif subtype == "K_15M":
                    data = ticker.history(period='7d', interval='15m')
                elif subtype == "K_5M":
                    data = ticker.history(period='7d', interval='30m')
                data['sub_type'] = subtype
                data['code'] = code
                data.columns = [c.lower() for c in data.columns]
                data.index = data.index.tz_localize(None)
                data.reset_index(inplace=True)
                data.set_index(['Datetime', 'code'], inplace=True)
                self.data = self.data.append(data)
                print(code, subtype)
        self.time_ = self.data.index.get_level_values(0).unique().to_list()

        return 0, 'subscribe: {} type: {} success'.format(code_list, subtype_list)


    def unsubscribe(self, code_list, subtype_list, *args, **kwargs):
        return 0, 'unsubscribe: {} type: {} success'.format(code_list, subtype_list)


    def get_trading_date(self, market, start, end, *args, **kwargs):
        super().get_trading_date(market, start, end, *args, **kwargs)


    def get_history_kline(self, symbol, start=None, end=None, kline_type=None, num=None, *args, **kwargs):
        time = self.cur_data.index.get_level_values(0).unique().to_list()[-num:]
        if kline_type is None:
            return 1, 'kline_type cannot be None'

        if start is None and end is None:
            if num is None:
                return 1, 'start, end and num cannot all be None'
            else:
                data = self.cur_data.loc[(time, [symbol]), :]
                data = data[data['sub_type'] == kline_type]
                data.index = data.index.droplevel(1)
                data['code'] = symbol
                return 0, data
        elif start is None and end is not None:
            raise NotImplementedError
        elif start is not None and end is None:
            raise NotImplementedError
        elif start is not None and end is not None:
            raise NotImplementedError


    def get_cur_kline(self, symbol, num, ktype, *args, **kwargs):
        time = self.cur_data.index.get_level_values(0).unique().to_list()[-num:]
        data = self.cur_data.loc[(time, [symbol]), :]
        data = data[data['sub_type'] == ktype]
        data.index = data.index.droplevel(1)
        data['code'] = symbol
        return 0, data


if __name__ == '__main__':
    quote = DemoQuote()
