from gateway.constant import KLType
from gateway.quote_base import QuoteBase
import fxcmpy
import pandas as pd
import datetime
from datetime import timedelta
import pytz
from collections import defaultdict
import plotly.io as pio

pio.renderers.default = "browser"
from graph.bar_component import candlestick
import plotly.graph_objects as go


class FxcmQuote(QuoteBase):
    name = 'fxcm'
    ohlc_key = ['open', 'high', 'low', 'close']
    cols = ['open', 'high', 'low', 'close', 'tickqty']
    ktype_fxcmKtype = {
        KLType.K_1M: 'm1',
        KLType.K_5M: 'm5',
        KLType.K_15M: 'm15',
        KLType.K_60M: 'H1',
        KLType.K_2H: 'H2',
        KLType.K_4H: 'H4',
        KLType.K_6H: 'H6',
        KLType.K_8H: 'H8',
        KLType.K_DAY: 'D1',
        KLType.K_WEEK: 'W1',
        KLType.K_MON: 'M1'

    }

    fre_dict = {
        KLType.K_1M: '1T',
        KLType.K_5M: '5T',
        KLType.K_15M: '15T',
        # KLType.K_60M: '30T',
        KLType.K_60M: '1H',
        KLType.K_2H: '2H',
        KLType.K_3H: '3H',
        KLType.K_4H: '4H',
        KLType.K_6H: '6H',
        KLType.K_8H: '8H',
        KLType.K_DAY: '1D',
        KLType.K_WEEK: '1W',
        KLType.K_MON: '1M'

    }

    # datetime.datetime.now(tz=pytz.timezone('nz'))

    def __init__(self, fxcm=None, access_token='', config_file='',
                 log_file=None, log_level='', server='demo',
                 proxy_url=None, proxy_port=None, proxy_type=None):
        super(FxcmQuote, self).__init__()
        self.subscribe_data = defaultdict()
        self.last = None
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

    def get_history_kline(self, symbol, start=None, end=None, kline_type=KLType.K_60M, num=10, *args,
                          **kwargs):
        if 'count' not in kline_type:
            try:
                data = self.con.get_candles(symbol, period=self.ktype_fxcmKtype[kline_type], number=num, start=start,
                                            end=end)
                for col in self.ohlc_key:
                    data[col] = (data['bid' + col] + data['ask' + col]) / 2
                data = data[self.cols]
                data['code'] = symbol
                data['k_type'] = kline_type
                return 1, data
            except ValueError:
                data = 'ValueError'
                return 0, data
        else:
            if start is not None or end is not None:
                return 0, 'For count bar start and end cannot be specific. '
            count = int(kline_type.replace('K_', '').replace('count', ''))
            dt = datetime.datetime.now()
            count_bar = self.get_history_count_bar(symbol, count, dt)
            while len(count_bar) < num:
                dt = dt - timedelta(days=7)
                cb = self.get_history_count_bar(symbol, count, dt)
                count_bar = cb.append(count_bar)
            return 1, count_bar[-num:]

    def get_symbol_basic_info(self, market, symbol_type, symbol_list=None, *args, **kwargs):
        pass

    def subscribe(self, code_list, subtype_list=None, add_callbacks=(), *args, **kwargs):
        # {'Updated': 1599441546176, 'Rates': [1.1837600000000001, 1.18387, 1.18499, 1.18309], 'Symbol': 'EUR/USD'}
        # df 2020-09-07 01:18:42.099  1.18376  1.18387  1.18499  1.18309
        if subtype_list is None:
            for code in code_list:
                self.con.subscribe_market_data(code, add_callbacks=add_callbacks)
            return 1, ''
        else:
            raise NotImplementedError

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

    def get_cur_kline(self, symbol, num=10, ktype=KLType.K_60M, *args, **kwargs):
        if self.is_subscribed(symbol)[1] is False:
            self.subscribe([symbol])

        _, data = self.get_history_kline(symbol, num=num, kline_type=ktype)
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
        data['k_type'] = ktype
        return 1, data[-num:]

    def get_this_week_history_kline(self, symbol, kline_type=KLType.K_60M):
        start = self._get_this_week_start_utc_time_of_week().replace(tzinfo=None)
        end = self._get_this_week_end_utc_time_of_week().replace(tzinfo=None)

        return self.get_history_kline(symbol, start=start, end=end, kline_type=kline_type,
                                      num=10000)

    def get_specific_week_history_kline(self, symbol, kline_type, dt: datetime.datetime):
        start = self._get_this_week_start_utc_time_of_week(dt)
        end = self._get_this_week_end_utc_time_of_week(dt)

        return self.get_history_kline(symbol, start, end, kline_type=kline_type, num=10000)

    def get_history_count_bar(self, symbol, count: int, dt: datetime.datetime or None = None):

        agg_dict = {'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'date': ['min', 'max'],
                    'tickqty': 'sum'
                    }
        if dt is None:
            _, count_bar = self.get_specific_week_history_kline(symbol, KLType.K_1M, datetime.datetime.now())
        else:
            _, count_bar = self.get_specific_week_history_kline(symbol, KLType.K_1M, dt)

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
        count_bar['code'] = symbol
        count_bar['k_type'] = 'K_' + str(count) + 'count'
        return count_bar

    @staticmethod
    def _get_this_week_start_utc_time_of_week(nz: datetime.datetime or None = None):
        if nz is None:
            nz = datetime.datetime.now(tz=pytz.timezone('nz'))
        start = (nz - timedelta(days=nz.weekday(), hours=nz.hour - 9, minutes=nz.minute, seconds=nz.second,
                                microseconds=nz.microsecond))
        utc_start = start.astimezone(pytz.utc).replace(tzinfo=None)
        return utc_start

    @staticmethod
    def _get_this_week_end_utc_time_of_week(nz: datetime.datetime or None = None):
        if nz is None:
            nz = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        end = (nz - timedelta(days=nz.weekday() - 4, hours=nz.hour - 17, minutes=nz.minute, seconds=nz.second,
                              microseconds=nz.microsecond))
        utc_end = end.astimezone(pytz.utc).replace(tzinfo=None)
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
    # _, data = fxcm_quote.get_this_week_history_kline('EUR/USD', 'm1')
    # count_bar = fxcm_quote.get_this_week_history_count_bar('EUR/USD', 3000)

    # go.Figure(candlestick(count_bar)).show()
