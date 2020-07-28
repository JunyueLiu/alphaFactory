import logging
import datetime as dt
import pickle
import json

from bar_manager.BarManager import BarManager
from gateway.brokerage_base import BrokerageBase
from gateway.quote_base import QuoteBase


class Strategy:
    backtesting = True

    def __init__(self):
        # strategy basic description
        self.strategy_name = ''
        self.author = ''
        self.strategy_version = ''
        self.strategy_description = ''

        # logger setting
        log_filename = dt.datetime.now().strftime('../logs/' + type(self).__name__ + "_%Y-%m-%d_%H_%M_%S.log")
        logging.basicConfig(level=logging.DEBUG,
                            format='|%(levelname)s|%(asctime)s|%(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=log_filename)
        self.logger = logging.getLogger(type(self).__name__ + '_backtesting' if self.backtesting else '_real')

        # K_line setting
        self.symbols = []
        self.k_1m = None
        self.k_3m = None
        self.k_5m = None
        self.k_15m = None
        self.k_30m = None
        self.k_60m = None
        self.k_4h = None
        self.k_8h = None
        self.k_1d = None
        self.k_1w = None

        # parameter setting
        self.ta_parameters = {}
        self.strategy_parameters = {}
        self.lookback_period = {}

        # trade related state variable
        self._quote_ctx = None  # type: QuoteBase
        self._brokerage_ctx = None  # type: BrokerageBase

        # strategy related state variables
        self.subscribe = {}
        self.position = 0
        self.same_bar_traded = False
        self.last_bar = {}
        self.traded_list = list()

        self.start = None
        self.end = None

    def set_quote_context(self, quote_context: QuoteBase):
        self._quote_ctx = quote_context  # type: QuoteBase

    def set_brokerage_context(self, brokerage_context: BrokerageBase):
        self._brokerage_ctx = brokerage_context  # type: BrokerageBase

    def set_trade_day(self):
        pass

    def init_kline_object(self):
        self.symbols = self.subscribe.keys()
        for key, value in self.subscribe.items():
            self.write_log_info('subscribe {}:{}'.format(key, value))
            self._quote_ctx.subscribe([key], value)
            for sub_type in value:
                sub_type_lower = sub_type.lower()
                if sub_type[0] == 'K':
                    if self.__dict__[sub_type_lower] is None:
                        self.__dict__[sub_type_lower] = dict()
                    self.__dict__[sub_type_lower][key] = BarManager(sub_type, self.lookback_period[key][sub_type],
                                                                    self.ta_parameters[key])
                elif sub_type == 'TICKER':
                    pass
                elif sub_type == 'QUOTE':
                    pass
                elif sub_type == 'ORDER_BOOK':
                    pass
                elif sub_type == 'RT_DATA':
                    pass
                elif sub_type == 'BROKER':
                    pass
                else:
                    self.__dict__[sub_type_lower] = None

    def load_setting(self, setting: dict or str):
        if isinstance(setting, dict):
            self.write_log_info('load setting from dict.')
            self.strategy_parameters = setting
        elif isinstance(setting, str):
            self.write_log_info('load setting from json.')
            with open(setting, 'rb') as f:
                df = f.read()
                f.close()
                self.strategy_parameters = json.loads(df)
        self.write_log_info('Setting loaded. Setting: {}'.format(self.strategy_parameters))
        d = self.__dict__
        for key in d.keys():
            if key in self.strategy_parameters.keys():
                d[key] = self.strategy_parameters[key]

    def load_history_data(self):
        self.write_log_info('load history data')
        for symbol, sub_types in self.subscribe.items():
            if self.backtesting:
                for sub in sub_types:
                    num = self.lookback_period[symbol][sub]
                    self.write_log_info('load backtesting data: {}:{} number:{}'.format(symbol, sub, num))
                    _, data = self._quote_ctx.get_history_kline(symbol, kline_type=sub, num=num)
                    self.__dict__[sub.lower()][symbol].init_with_pandas(data)
            else:
                self.write_log_info('load history data: {}:{}:{}:{}')

    def process_kline(self, data):
        for ix, row in data.iterrows():
            code = row['code']
            if row['k_type'] == 'K_1M':
                if self.last_bar['K_1M'] < ix:  # new bar comes in
                    self.on_1min_bar(self.k_1m)
                    self.last_bar['K_1M'] = ix
                    self.k_1m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_1m[code].update_with_pandas(row, time_key='time_key')
                    self.on_1min_bar(self.k_1m)
            elif row['k_type'] == 'K_5M':
                if self.last_bar['K_5M'] < ix:  # new bar comes in
                    # self.same_bar_traded = False
                    self.on_5min_bar(self.k_5m)
                    self.last_bar['K_5M'] = ix
                    self.k_5m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_5m[code].update_with_pandas(row, time_key='time_key')
                    self.on_5min_bar(self.k_5m)
            elif row['k_type'] == 'K_15M':
                if self.last_bar['K_15M'] < ix:  # new bar comes in
                    # self.same_bar_traded = False
                    self.on_15min_bar(self.k_15m)
                    self.last_bar['K_15M'] = ix
                    self.k_15m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_15m[code].update_with_pandas(row, time_key='time_key')
                    self.on_15min_bar(self.k_15m)
            elif row['k_type'] == 'K_30M':
                if self.last_bar['K_30M'] < ix:  # new bar comes in
                    # self.same_bar_traded = False
                    self.on_30min_bar(self.k_30m)
                    self.last_bar['K_30M'] = ix
                    self.k_30m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_30m[code].update_with_pandas(row, time_key='time_key')
                    self.on_30min_bar(self.k_30m)
            elif row['k_type'] == 'K_60M':
                if self.last_bar['K_60M'] < ix:  # new bar comes in
                    # self.same_bar_traded = False
                    self.on_60min_bar(self.k_60m)
                    self.last_bar['K_60M'] = ix
                    self.k_60m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_60m[code].update_with_pandas(row, time_key='time_key')
                    self.on_60min_bar(self.k_60m)
            self.logger.info('process_kline for {} {}'.format(ix, code))

    def strategy_logic(self, data):
        pass

    def on_strategy_init(self, datetime):
        self.write_log_info(
            'start to initial strategy {} {} at time {}'.format(self.strategy_name, self.strategy_version, datetime))

        self.write_log_info('strategy current mode:{}, Exchange:{}, brokerage:{}'.format(
            'backtesting' if self.backtesting else 'real', self._brokerage_ctx.exchange_name, self._brokerage_ctx.name))
        self.init_kline_object()
        self.load_history_data()
        self.write_log_info('finish initiation.')

    def on_before_trade_day(self, datetime):
        pass

    def on_after_trade_day(self, datetime):
        pass

    def on_1min_bar(self, bar):
        pass

    def on_5min_bar(self, bar):
        pass

    def on_15min_bar(self, bar):
        pass

    def on_30min_bar(self, bar):
        pass

    def on_60min_bar(self, bar):
        pass

    def on_4h_bar(self, bar):
        pass

    def on_8h_bar(self, bar):
        pass

    def on_day_bar(self, bar):
        pass

    def on_quote(self, quote):
        pass

    def on_order_send(self):
        pass

    def on_order_status_change(self, *args, **kwargs):
        pass

    def buy(self, symbol, price, vol, order_type, *args, **kwargs):
        self.write_log_info('Buy {} at {}, amount {}'.format(symbol, price, str(vol)))
        self._brokerage_ctx.place_order(price, vol, symbol, 'LONG', order_type=order_type)

    def sell(self, symbol, price, vol, order_type, *args, **kwargs):
        self.write_log_info('Sell {} at {}, amount {}'.format(symbol, price, str(vol)))
        self._brokerage_ctx.place_order(price, vol, symbol, 'SHORT', order_type=order_type)

    def short(self, symbol, price, vol, order_type, *args, **kwargs):
        self.write_log_info('Short {} at {}, amount {}'.format(symbol, price, str(vol)))
        self._brokerage_ctx.place_order(price, vol, symbol, 'SHORT', order_type=order_type)

    def cover(self, symbol, price, vol, order_type, *args, **kwargs):
        self.write_log_info('Cover {} at {}, amount {}'.format(symbol, price, str(vol)))
        self._brokerage_ctx.place_order(price, vol, symbol, 'LONG', order_type=order_type)

    def cancel_all(self):
        self._brokerage_ctx.cancel_all_order()

    def modified_order(self, order_id):
        pass

    def _update_traded_list(self, trade):
        self.traded_list.append(trade)

    def _update_indicators(self, all=True):
        pass

    def write_log_info(self, content):
        self.logger.info(content)

    def write_log_error(self, content):
        self.logger.error(content)

    def write_log_debug(self, content):
        self.logger.debug(content)


class DayTradeStrategy(Strategy):
    def __init__(self):
        super(DayTradeStrategy, self).__init__()
