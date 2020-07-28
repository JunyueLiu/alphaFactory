from gateway.quote_base import QuoteBase
import pandas as pd


class BacktestingQuote(QuoteBase):
    def __init__(self, data: dict = None):

        super().__init__()
        self.history_data = data
        self.subscribe_dict = {}

    def set_history_data(self, data: dict):
        self.history_data = data

    def subscribe(self, code_list: list, subtype_list: list, *args, **kwargs):
        for code in code_list:
            for subtype in subtype_list:
                try:
                    if code in self.subscribe_dict.keys():
                        self.subscribe_dict[code].append(subtype)
                    else:
                        self.subscribe_dict[code] = [subtype]
                except KeyError:
                    self.subscribe_dict = {}
                    return 0, 'subscribe failure: the history data is not provided for {}:{}'.format(code, subtype)
        return 1, None

    def unsubscribe(self, code_list, subtype_list, *args, **kwargs):
        for code in code_list:
            for subtype in subtype_list:
                try:
                    self.subscribe_dict[code].remove(subtype)
                except:
                    return 0, '{}:{} not in subscribe list'.format(code, subtype)
                if len(self.subscribe_dict[code]) == 0:
                    del self.subscribe_dict[code]
        return 1, None

    def unsubscribe_all(self):
        self.subscribe_dict = {}
        return 1, None

    def get_history_kline(self, symbol, start=None, end=None, kline_type='k_1D', num=1000, *args, **kwargs):
        if symbol in self.subscribe_dict.keys():
            df = self.history_data[symbol][kline_type]
            if start is not None:
                df = df[df.index >= pd.to_datetime(start)]
            if end is not None:
                df = df[df.index < pd.to_datetime(end)]
            df = df[-num:]
            return 1, df
        else:
            return 0, 'The {} is not subscribed.'.format(symbol)

    def get_cur_kline(self, symbol, num, ktype, *args, **kwargs):
        if symbol in self.subscribe_dict.keys():
            df = self.history_data[symbol][ktype]
            df = df[-num:]
            return 1, df
        else:
            return 0, 'The {} is not subscribed.'.format(symbol)

    def query_subscription(self):
        pass

    def get_stock_quote(self):
        pass

    def get_trading_date(self, market, start, end, *args, **kwargs):
        pass

    def get_market_snapshot(self, symbol_list, date=None, **kwargs):
        pass

