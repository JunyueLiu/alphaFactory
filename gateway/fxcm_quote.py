from threading import Thread
from typing import Optional, Dict, List, Type

from gateway.constant import KLType
from gateway.quote_base import QuoteBase
import fxcmpy
import pandas as pd
import datetime
import time
from datetime import timedelta
import pytz
from collections import defaultdict
import plotly.io as pio

pio.renderers.default = "browser"
from graph.bar_component import candlestick
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')


class FXCMHandlerBase(object):

    @staticmethod
    def on_recv_rsp(self, data: pd.DataFrame):
        pass


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
        self.bar_data: Optional[Dict[str, Dict[str, pd.DataFrame]]] = defaultdict(dict)
        self.handlers: List[Type[FXCMHandlerBase]] = []
        self.threads: List[Thread] = []
        self._last_1min_bar_request = None
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
            while True:
                try:
                    data = self.con.get_candles(symbol, period=self.ktype_fxcmKtype[kline_type], number=num,
                                                start=start,
                                                end=end)
                    for col in self.ohlc_key:
                        data[col] = (data['bid' + col] + data['ask' + col]) / 2
                    data = data[self.cols]
                    data['code'] = symbol
                    data['k_type'] = kline_type
                    if len(data) == 0:
                        # self.con.__reconnect__(10)
                        print('no data')
                        time.sleep(1)
                        continue
                    return 1, data
                except ValueError:
                    data = 'ValueError'
                    print(data)
                    return 0, data
                except IOError:
                    self.con.__reconnect__(10)
                except Exception as e:
                    # data = 'Unknown Error'
                    print(e)
                    # return 0, data
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

    def update_count_bar(self, count_bar: pd.DataFrame) -> pd.DataFrame:
        # todo new bar logic should apply to trader part (use date_start to tell, date == date_start)
        # print('update_count_bar')
        symbol = count_bar['code'][0]
        count_now = count_bar['tickqty'][-1]
        start = count_bar['date_start'][-1]
        count = int(count_bar['k_type'][-1].replace('K_', '').replace('count', ''))

        _, m1_bar = self.get_cur_kline(symbol, num=500, kline_type=KLType.K_1M)
        if _ == 0 or len(m1_bar) == 0:
            return count_bar
        # print(m1_bar)
        # m1_bar = m1_bar[m1_bar.index >= start]

        if count_now < count:
            count_bar = count_bar[:-1]

        m1_bar.index.name = 'date'
        m1_bar.reset_index(inplace=True)

        agg_dict = {'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'date': ['min', 'max'],
                    'tickqty': 'sum'
                    }
        m1_bar['group'] = len(count_bar)
        bar_sample = 0
        cum_tick = 0
        for index, value in m1_bar.iterrows():
            cum_tick += value['tickqty']
            m1_bar['group'].loc[index] = bar_sample
            if cum_tick >= count:
                cum_tick = 0
                bar_sample += 1

        new_count_bar = m1_bar.reset_index().groupby('group').agg(agg_dict)
        new_count_bar.columns = ['open',
                                 'high',
                                 'low',
                                 'close',
                                 'date_start',
                                 'date',
                                 'tickqty']
        new_count_bar.set_index('date', inplace=True)
        new_count_bar['code'] = symbol
        new_count_bar['k_type'] = 'K_' + str(count) + 'count'
        count_bar = count_bar.append(new_count_bar)
        count_bar = count_bar[count_bar['tickqty'] > 0]
        count_bar = count_bar[~count_bar.index.duplicated(keep='first')]
        # print('updated', count_bar)
        return count_bar

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
            for code in code_list:
                for sub in subtype_list:
                    if 'count' not in sub:
                        if len(add_callbacks) > 0:
                            for func in add_callbacks:
                                t = Thread(target=self.__subscribe_time_bar, args=(code, sub, func),
                                           name='{}_{}_{}'.format(code, sub, func.__name__))
                                self.threads.append(t)
                        else:
                            t = Thread(target=self.__subscribe_time_bar, args=(code, sub),
                                       name='{}_{}'.format(code, sub))
                            self.threads.append(t)
                    else:
                        t = Thread(target=self.__subscribe_time_bar, args=(code, KLType.K_1M),
                                   name='{}_{}'.format(code, KLType.K_1M))
                        self.threads.append(t)

                        if len(add_callbacks) > 0:
                            for func in add_callbacks:
                                t = Thread(target=self.__subscribe_count_bar, args=(code, sub, func),
                                           name='{}_{}_{}'.format(code, sub, func.__name__))
                                self.threads.append(t)

                        else:
                            t = Thread(target=self.__subscribe_count_bar, args=(code, sub),
                                       name='{}_{}'.format(code, sub))
                            self.threads.append(t)
            for t in self.threads:
                if not t.is_alive():
                    t.start()

            return 1, ''

    def unsubscribe(self, code_list, subtype_list=None, *args, **kwargs):
        # super().unsubscribe(code_list, subtype_list, *args, **kwargs)
        for t in self.threads:
            t.join()

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

    def get_cur_kline(self, symbol, num=10, kline_type=KLType.K_60M, *args, **kwargs):
        if self.is_subscribed(symbol)[1] is False:
            self.subscribe([symbol])
        if 'count' not in kline_type:
            while True:
                try:
                    start = kwargs['start'] if 'start' in kwargs else None
                    # end = kwargs['end'] if 'end' in kwargs else None
                    _, data = self.get_history_kline(symbol, num=num, kline_type=kline_type, start=start)
                    # print(data)
                    if _ == 0:
                        return 0, data
                    break
                except Exception as e:
                    print(e)
                    return 0, e
            cur = data.index[-1]
            _, updated = self.get_prices(symbol)
            updated = updated[updated.index > cur]

            if len(updated) > 0:
                updated = updated[['mp']]
                updated = updated.groupby(pd.Grouper(freq=self.fre_dict[kline_type])).agg('ohlc')
                updated.columns = updated.columns.get_level_values(1)
                if updated.index[-1] == cur:
                    data.update(updated)
                else:
                    updated = updated[updated.index > cur]
                    updated['tickqty'] = 0
                    data = data.append(updated)
            data['code'] = symbol
            data['k_type'] = kline_type
            return 1, data[-num:]
        else:
            if symbol not in self.bar_data or kline_type not in self.bar_data[symbol]:
                # _, data = self.get_history_kline(symbol, kline_type=kline_type, num=num)
                self.__subscribe_count_bar(symbol, kline_type)

            data = self.bar_data[symbol][kline_type].iloc[-num:]
            return 1, data

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
                             'date_start',
                             'date',
                             'tickqty']
        count_bar.set_index('date', inplace=True)
        count_bar['code'] = symbol
        count_bar['k_type'] = 'K_' + str(count) + 'count'
        return count_bar

    @staticmethod
    def _get_this_week_start_utc_time_of_week(nz: datetime.datetime or None = None):
        """
        FXCM is open for trade continuously during all of the above listed periods on a 24-hour per day, 5-day per week
        basis. Trading operations may be conducted via FXCM brokerage anytime between open and close:
        Open: Sundays, between 5:00 and 5:15 pm EST
        :param nz:
        :return:
        """
        if nz is None:
            nz = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        if nz.weekday() == 6:
            start = (nz - timedelta(hours=nz.hour - 17, minutes=nz.minute, seconds=nz.second,
                                    microseconds=nz.microsecond
                                    ))
        else:
            start = (nz - timedelta(days=nz.weekday() + 1, hours=nz.hour - 17, minutes=nz.minute, seconds=nz.second,
                                    microseconds=nz.microsecond))
        utc_start = start.astimezone(pytz.utc).replace(tzinfo=None)
        return utc_start

    @staticmethod
    def _get_this_week_end_utc_time_of_week(nz: datetime.datetime or None = None):
        """
        Close: Fridays, around 4:55 pm EST
        :param nz:
        :return:
        """
        if nz is None:
            nz = datetime.datetime.now(tz=pytz.timezone('US/Eastern'))
        if nz.weekday() == 6:
            end = nz - timedelta(hours=nz.hour - 17, minutes=nz.minute, seconds=nz.second,
                                 microseconds=nz.microsecond) + timedelta(days=5)
        else:
            end = (nz - timedelta(days=nz.weekday() - 4, hours=nz.hour - 17, minutes=nz.minute, seconds=nz.second,
                                  microseconds=nz.microsecond))
        utc_end = end.astimezone(pytz.utc).replace(tzinfo=None)
        return utc_end

    def is_trading(self):
        # Open: Sundays, between 5:00 and 5:15 pm EST
        # Close: Fridays, around 4:55 pm EST
        utc_start = self._get_this_week_start_utc_time_of_week()
        utc_end = self._get_this_week_end_utc_time_of_week()
        now = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None)
        if utc_start <= now <= utc_end:
            return True
        else:
            return False

    def set_handler(self, handler: Type[FXCMHandlerBase]):
        self.handlers.append(handler)

    def make_count_bar(self, m1_bar: pd.DataFrame, count):
        symbol = m1_bar['code'].iloc[0]
        count_bar = m1_bar.copy()

        agg_dict = {'open': 'first',
                    'high': 'max',
                    'low': 'min',
                    'close': 'last',
                    'date': ['min', 'max'],
                    'tickqty': 'sum'
                    }
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
                             'date_start',
                             'date',
                             'tickqty']
        count_bar = count_bar.set_index('date')
        count_bar['code'] = symbol
        count_bar['k_type'] = 'K_' + str(count) + 'count'
        return count_bar

    def __subscribe_time_bar(self, symbol, kline_type, func=None):
        if symbol not in self.bar_data or kline_type not in self.bar_data[symbol]:
            _, data = self.get_this_week_history_kline(symbol, kline_type)
            self.bar_data[symbol][kline_type] = data
            push = True
            while True:
                data = self.bar_data[symbol][kline_type]
                now = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None)
                if now > data.index[-1] and push:
                    _, new_data = self.get_history_kline(symbol, kline_type=kline_type, num=10)
                    data.update(new_data)
                    self.bar_data[symbol][kline_type] = data
                    push_bar = data[-1:]
                    for handler in self.handlers:
                        handler.on_recv_rsp(self, push_bar)
                    if func is not None:
                        func(push_bar)
                    push = False
                    second = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None).second
                    if second < 30:
                        time.sleep(30 - second)
                elif not push and (now - data.index[-1]).seconds >= 90:
                    _, new_data = self.get_history_kline(symbol, kline_type=kline_type, num=10)
                    if new_data.index[-1] > data.index[-1]:
                        appended_data = new_data.loc[new_data.index.difference(data.index)]
                        data = data.append(appended_data)
                        data.update(new_data)
                        self.bar_data[symbol][kline_type] = data
                    push = True
                    second = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None).second
                    time.sleep(60 - second)
                else:
                    time.sleep(1)
        else:
            print('already subscribe..')
            return

    def __subscribe_count_bar(self, symbol, kline_type, func=None):
        # last_dt = None  # type: Optional[pd.Timestamp]
        # if not self.is_trading():
        #     print('not trading time. exit')
        #     return
        count = int(kline_type.replace('K_', '').replace('count', ''))
        while KLType.K_1M not in self.bar_data[symbol]:
            time.sleep(1)
        count_bar = self.make_count_bar(self.bar_data[symbol][KLType.K_1M], count)
        self.bar_data[symbol][kline_type] = count_bar
        push = True
        while True:
            count_bar = self.bar_data[symbol][kline_type]
            if push and count_bar.iloc[-1]['tickqty'] >= count:
                push_bar = count_bar[-1:]
                for handler in self.handlers:
                    handler.on_recv_rsp(self, push_bar)
                if func is not None:
                    func(push_bar)
                new_count_bar = pd.DataFrame()
                count_bar_start = push_bar.index[0] + pd.Timedelta(minutes=1)
                push = False
            else:
                new_count_bar = count_bar.iloc[[-1]]
                count_bar_start = new_count_bar['date_start'].iloc[0]

            # update count bar
            # control time
            second = datetime.datetime.now(tz=pytz.utc).replace(tzinfo=None).second
            time.sleep(61 - second)
            m1_data = self.bar_data[symbol][KLType.K_1M]
            new_m1_data = m1_data.loc[count_bar_start:]
            if len(new_m1_data) > 0:
                temp_new_count_bar = self.make_count_bar(new_m1_data, count)
                if len(new_count_bar) > 0:
                    count_bar = count_bar.iloc[:-1]
                count_bar = count_bar.append(temp_new_count_bar)
                self.bar_data[symbol][kline_type] = count_bar
                push = True
            else:
                push = False


if __name__ == '__main__':
    fxcm_quote = FxcmQuote(config_file='../gateway/fxcm_config/demo_config')
    # _, data = fxcm_quote.get_history_kline('EUR/USD', kline_type=KLType.K_2000count, num=100)
    pd.set_option('max_columns', None)


    # def to_dict(df: pd.DataFrame):
    #     records = df.to_dict('index')
    #     print(records)
    #
    class PrinterHandler(FXCMHandlerBase):
        def on_recv_rsp(self, data: pd.DataFrame):
            for idx, row in data.iterrows():
                if 'count' in row['k_type']:
                    print('{} {} {} {} {}'.format(idx, row['date_start'], row['tickqty'], row['code'], row['k_type']))
                else:
                    print('{} {} {} {}'.format(idx, row['tickqty'], row['code'], row['k_type']))
            # records = data.to_dict('index')
            # print(records)


    #
    fxcm_quote.set_handler(PrinterHandler)
    fxcm_quote.subscribe(['EUR/USD', 'USD/JPY'], [KLType.K_1000count])
    # last_dt = None  # type: Optional[pd.Timestamp]
    # last_count = 0
    # while True:
    #     start = datetime.datetime.now()
    #     start_utc = datetime.datetime.now(tz=pytz.utc).replace(second=0, microsecond=0, tzinfo=None)
    #     # if last_dt is not None and start_utc == last_dt.to_pydatetime():
    #     #     time.sleep(1)
    #     #     continue
    #     _, data = fxcm_quote.get_cur_kline('EUR/USD', 10, KLType.K_1000count)
    #     end = datetime.datetime.now()
    #     if _ == 1 and last_count != data['tickqty'].iloc[-1]:
    #         last_dt = data.index[-1]
    #         last_count = data['tickqty'].iloc[-1]
    #         print(data[-1:])
    #         print('*' * 20)
    #     time.sleep(2)
    # last_row = data.iloc[-1:]
    # pd.set_option('max_columns', None)
    # while True:
    #     data = fxcm_quote.update_count_bar(data)
    #     if len(data) > 0:
    #         data = data.iloc[-100:]
    #     print(data[-1:])
    #     time.sleep(5)

    # go.Figure(candlestick(count_bar)).show()
