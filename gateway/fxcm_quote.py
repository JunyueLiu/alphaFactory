from gateway.quote_base import QuoteBase
import fxcmpy
import pandas as pd
import datetime
from datetime import timedelta
import pytz

import plotly.io as pio

pio.renderers.default = "browser"
from graph.bar_component import candlestick
import plotly.graph_objects as go


class FxcmQuote(QuoteBase):
    name = 'fxcm'
    ohlc_key = ['open', 'high', 'low', 'close']
    cols = ['open', 'high', 'low', 'close', 'tickqty']
    fre_dict = {
        'm1': '1T',
        'm5': '5T',
        'm15': '15T',
        'm30': '30T',
        'H1': '1H',
        'H2': '2H',
        'H3': '3H',
        'H4': '4H',
        'H6': '6H',
        'H8': '8H',
        'D1': '1D',
        'W1': '1W',
        'M1': '1M'

    }

    # datetime.datetime.now(tz=pytz.timezone('nz'))

    def __init__(self, fxcm=None, access_token='', config_file='',
                 log_file=None, log_level='', server='demo',
                 proxy_url=None, proxy_port=None, proxy_type=None):
        super(FxcmQuote, self).__init__()
        if fxcm is None:
            self.con = fxcmpy.fxcmpy(access_token=access_token, config_file=config_file,
                                     log_file=log_file, log_level=log_level, server=server,
                                     proxy_url=proxy_url, proxy_port=proxy_port, proxy_type=proxy_type)
        else:
            self.con = fxcm  # type: fxcmpy.fxcmpy

    def get_instruments(self):
        return 1, self.con.get_instruments()

    def get_market_snapshot(self, symbol_list=None, *args, **kwargs):
        try:
            offers = self.con.get_offers()
            return 1, offers
        except ValueError:
            offers = 'ValueError'
            return 0, offers

    def get_history_kline(self, symbol, start=None, end=None, kline_type='H1', num=10, *args, **kwargs):
        try:
            data = self.con.get_candles(symbol, period=kline_type, number=num, start=start, end=end)
            for col in self.ohlc_key:
                data[col] = (data['bid' + col] + data['ask' + col]) / 2
            data = data[self.cols]
            data['code'] = symbol
            data['k_type'] = 'K_' + kline_type[-1] + kline_type[0]
            return 1, data
        except ValueError:
            data = 'ValueError'
            return 0, data

    def get_symbol_basic_info(self, market, symbol_type, symbol_list=None, *args, **kwargs):
        pass

    def subscribe(self, code_list, subtype_list=None, add_callbacks=(), *args, **kwargs):
        # {'Updated': 1599441546176, 'Rates': [1.1837600000000001, 1.18387, 1.18499, 1.18309], 'Symbol': 'EUR/USD'}
        # df 2020-09-07 01:18:42.099  1.18376  1.18387  1.18499  1.18309
        for code in code_list:
            self.con.subscribe_market_data(code, add_callbacks=add_callbacks)
        return 1, ''

    def unsubscribe(self, code_list, subtype_list=None, *args, **kwargs):
        # super().unsubscribe(code_list, subtype_list, *args, **kwargs)
        for code in code_list:
            self.con.unsubscribe_market_data(code)
        return 1, ''

    def unsubscribe_all(self, *args, **kwargs):
        for code in self.con.get_subscribed_symbols():
            self.con.unsubscribe_market_data(code)
        return 1, ''

    def subscribe_instrument(self, symbol):
        return 1, self.con.subscribe_instrument(symbol)

    def unsubscribe_instrument(self, symbol):
        return 1, self.con.unsubscribe_instrument(symbol)

    def query_subscription(self, *args, **kwargs):
        return 1, self.con.get_subscribed_symbols()

    def is_subscribed(self, symbol):
        return 1, self.con.is_subscribed(symbol)

    def get_prices(self, symbol):
        data = self.con.get_prices(symbol=symbol)
        data['mp'] = (data['Bid'] + data['Ask']) / 2
        return 1, data[['mp', 'Bid', 'Ask']]

    def get_cur_kline(self, symbol, num=10, ktype='H1', *args, **kwargs):
        if self.is_subscribed(symbol)[1] is False:
            self.subscribe([symbol])

        _, data = self.get_history_kline(symbol, num=num - 1, kline_type=ktype)
        cur = data.index[-1]
        _, updated = self.get_prices(symbol)
        updated = updated[updated.index > cur]

        if len(updated) > 0:
            updated = updated[['mp']]
            updated = updated.groupby(pd.Grouper(freq=self.fre_dict[ktype])).agg('ohlc')
            updated.columns = updated.columns.get_level_values(1)
            if updated.index[-1] == cur:
                data.update(updated)
            else:
                updated = updated[updated.index > cur]
                updated['tickqty'] = 0
                data = data.append(updated)
        data['code'] = symbol
        data['k_type'] = 'K_' + ktype[-1] + ktype[0]
        return 1, data

    def get_this_week_history_kline(self, symbol, kline_type='H1'):
        start = self._get_this_week_start_utc_time_of_week().replace(tzinfo=None)
        end = self._get_this_week_end_utc_time_of_week().replace(tzinfo=None)

        return self.get_history_kline(symbol, start=start, end=end, kline_type=kline_type, num=10000)

    def get_this_week_history_count_bar(self, symbol, count: int):

        agg_dict = {'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'date': ['min', 'max'],
                    'tickqty': 'sum'
                    }
        _, count_bar = self.get_this_week_history_kline(symbol, 'm1')

        count_bar['group'] = len(count_bar)
        bar_sample = 0
        cum_tick = 0
        for index, value in count_bar.iterrows():
            cum_tick += value['tickqty']
            count_bar['group'].loc[index] = bar_sample
            if cum_tick >= count:
                cum_tick = 0
                bar_sample += 1

        count_bar = count_bar.reset_index().groupby('group').agg(agg_dict)

        count_bar.columns = ['open',
                             'high',
                             'low',
                             'close',
                             'date' + '_start',
                             'date',
                             'tickqty']
        count_bar.set_index('date', inplace=True)
        data['code'] = symbol
        data['k_type'] = 'K_' + str(count) + 'count'
        return count_bar

    @staticmethod
    def _get_this_week_start_utc_time_of_week(nz: datetime.datetime or None = None):
        if nz is None:
            nz = datetime.datetime.now(tz=pytz.timezone('nz'))
        start = (nz - timedelta(days=nz.weekday(), hours=nz.hour - 9, minutes=nz.minute, seconds=nz.second,
                                microseconds=nz.microsecond))
        utc_start = start.astimezone(pytz.utc)
        return utc_start

    @staticmethod
    def _get_this_week_end_utc_time_of_week(nz: datetime.datetime or None = None):
        if nz is None:
            nz = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        end = (nz - timedelta(days=nz.weekday() - 4, hours=nz.hour - 17, minutes=nz.minute, seconds=nz.second,
                              microseconds=nz.microsecond))
        utc_end = end.astimezone(pytz.utc)
        return utc_end

    def is_trading(self):
        # from monday 9 am of New Zealand/Wellington time to Friday 5 pm of US / Eastern time

        utc_start = self._get_this_week_start_utc_time_of_week()
        utc_end = self._get_this_week_end_utc_time_of_week()
        now = datetime.datetime.now(tz=pytz.utc)
        if utc_start <= now <= utc_end:
            return True
        else:
            return False


if __name__ == '__main__':
    fxcm_quote = FxcmQuote(config_file='../gateway/fxcm_config/demo_config')
    _, data = fxcm_quote.get_this_week_history_kline('EUR/USD', 'm1')
    count_bar = fxcm_quote.get_this_week_history_count_bar('EUR/USD', 3000)

    go.Figure(candlestick(count_bar)).show()
