import json
import datetime
import pandas as pd
import numpy as np
from numba import njit
# from backtesting.Exchange import *
from strategy.DoubleMA import DoubleMA
from gateway.quote_base import QuoteBase
from gateway.brokerage_base import BrokerageBase
from backtesting.BacktestingQuote import BacktestingQuote
from backtesting.BacktestingBrokerage import BacktestingBrokerage
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class BacktestingBase:
    def __init__(self, quote: BacktestingQuote, brokerage: BacktestingBrokerage, strategy: Strategy, strategy_parameter
                 , start=None, end=None, initial_capital=100, backtesting_setting=None):
        self.quote_ctx = quote
        self.brokerage_ctx = brokerage
        self.strategy = strategy
        self.strategy_parameter = strategy_parameter
        self.start = start
        self.end = end
        self.initial_capital = initial_capital
        self.backtesting_setting = backtesting_setting

        self.data = None

        self.dealt_list = []

        if self.start is None:
            self.start = self.backtesting_setting.get('start', None)
        if self.end is None:
            self.end = self.backtesting_setting.get('end', None)

    def _check_data_valid(self):
        """
        Check whether the data provided for backtesting is enough for strategy subscription
        :return:
        """
        for symbol, subtype_data in self.data.items():
            if symbol not in self.strategy_parameter['subscribe'].keys():
                raise ValueError('The data for backtesting doesn\'t include {}', symbol)
            else:
                for s in self.strategy_parameter['subscribe'][symbol]:
                    if s not in subtype_data.keys():
                        raise ValueError('The data for backtesting doesn\'t include {}:{}', symbol, s)

    def _initial_strategy(self):
        """
        To initial strategy, call before run the backtesting
        :return:
        """
        self.strategy.load_setting(self.strategy_parameter)
        self.strategy.set_quote_context(self.quote_ctx)
        self.strategy.set_brokerage_context(self.brokerage_ctx)

    def _load_setting(self, setting: dict or str):
        if isinstance(setting, dict):
            self.backtesting_setting = setting
        elif isinstance(setting, str):
            with open(setting, 'rb') as f:
                df = f.read()
                f.close()
                self.backtesting_setting = json.loads(df)
        d = self.__dict__
        for key in d.keys():
            if key in self.backtesting_setting.keys():
                d[key] = self.backtesting_setting[key]

    def _load_data(self):
        """

        :return:
        """
        self.data = dict()
        if self.backtesting_setting['data_source'] == 'csv':
            time_key = self.backtesting_setting['time_key']
            for symbol, bar_data in self.backtesting_setting['data'].items():
                self.data[symbol] = dict()
                for bar_type, path in bar_data.items():
                    bar = pd.read_csv(path)
                    bar[time_key] = pd.to_datetime(bar[time_key])
                    bar.set_index(time_key, inplace=True)
                    if self.start is not None:
                        bar = bar[bar.index >= pd.to_datetime(self.start)]
                    if self.end is not None:
                        bar = bar[bar.index <= pd.to_datetime(self.end)]
                    self.data[symbol][bar_type] = bar
        elif self.backtesting_setting['data_source'] == 'db':
            pass
        self.quote_ctx.set_history_data(self.data)

    def _reset_data(self):
        self.data = None

    def get_trading_history(self):
        return self.brokerage_ctx.history_order_list_query()

    def get_dealt_history(self):
        return self.brokerage_ctx.deal_order_list

    def _load_data_from_db(self):
        pass

    def _load_data_from_csv(self):
        pass

    def calculate_result(self):
        # first make the all asset price dataframe
        dfs = []
        for code, ktype_data in self.data.items():
            for ktype, data in ktype_data.items():
                d = data.reset_index()
                dfs.append(d)
        # print(self.backtesting_setting['time_key'])
        asset_price = pd.concat(dfs)
        asset_price.set_index(['code', self.backtesting_setting['time_key']], inplace=True)
        self.asset_price = asset_price
        self.dealt_list = self.get_dealt_history()
        # todo evaluate backtesting result
        traded = pd.DataFrame([order.order_dict() for order in self.dealt_list])
        traded['dealt_qty'] = np.where(traded['order_direction'] == 'LONG', traded['dealt_qty'], -traded['dealt_qty'])
        traded['dealt_outflow'] = - traded['dealt_price'] * traded['dealt_qty']
        traded_grouped = traded.groupby(['code', 'update_time', 'order_direction']).agg(
            {'dealt_outflow': 'sum', 'dealt_qty': 'sum'})
        traded_grouped.reset_index([2], inplace=True)
        traded_grouped = traded_grouped.groupby(level=[0]).cumsum()

        # print(traded_grouped)

    def run(self):
        pass


class DayTradeBacktesting(BacktestingBase):
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter):
        super(DayTradeBacktesting, self).__init__(quote, brokerage, strategy, strategy_parameter)


class VectorizedBacktesting(BacktestingBase):
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter, start=None,
                 end=None,
                 initial_capital=100, backtesting_setting=None):
        super(VectorizedBacktesting, self).__init__(quote, brokerage, strategy, strategy_parameter, start=start,
                                                    end=end,
                                                    initial_capital=initial_capital,
                                                    backtesting_setting=backtesting_setting)
        self.full_picture_bar_manager = dict()
        self.strategy_lookback_period = None

        self.time_list = np.empty(1, dtype='datetime64')
        self.state_generators = dict()
        self.state = dict()
        self.bar_timestamp = dict()
        self.min_timestamp = None
        self.kline_type_on_bar_match: dict = None

    def _load_data(self):
        super(VectorizedBacktesting, self)._load_data()
        for klines in self.data.values():
            for k in klines.keys():
                self.full_picture_bar_manager[k] = dict()

        for symbol, klines in self.data.items():
            for kline_type, data in klines.items():
                self.full_picture_bar_manager[kline_type][symbol] = BarManager(kline_type,
                                                                               size=len(data),
                                                                               ta_parameters=
                                                                               self.strategy.ta_parameters[symbol])
                self.full_picture_bar_manager[kline_type][symbol].init_with_pandas(data)  # type:BarManager

    def _initial_strategy(self):
        super()._initial_strategy()
        self.strategy_lookback_period = self.strategy.lookback_period
        self.kline_type_on_bar_match = {
            'K_1M': self.strategy.on_1min_bar,
            'K_5M': self.strategy.on_5min_bar,
            'K_15M': self.strategy.on_15min_bar,
            'K_30M': self.strategy.on_30min_bar,
            'K_60M': self.strategy.on_60min_bar,
            'K_4H': self.strategy.on_4h_bar,
            'K_8H': self.strategy.on_8h_bar

        }

    def _infer_time(self):
        """
        Infer all the timestamp from the data input.
        :return:
        """
        self.time_list = np.empty(0, dtype='datetime64')
        for symbol, subs in self.data.items():
            for v in subs.values():
                self.time_list = np.append(self.time_list, v.index.values)
        self.time_list = np.unique(self.time_list)
        self.time_list.sort()

    # @njit
    def generate_bar_manager_state(self, bar_manager: BarManager, size):
        """

        :param bar_manager:
        :param size:
        :return:
        """
        partial_bar_manager = BarManager(bar_manager.bar_name, size, None)
        partial_bar_manager.technical_indicator_parameters = bar_manager.technical_indicator_parameters
        partial_bar_manager.ta = dict()
        for i in range(bar_manager.size - size):
            partial_bar_manager.time = bar_manager.time[i: i + size]
            partial_bar_manager.open = bar_manager.open[i: i + size]
            partial_bar_manager.high = bar_manager.high[i: i + size]
            partial_bar_manager.low = bar_manager.low[i: i + size]
            partial_bar_manager.close = bar_manager.close[i: i + size]
            for k, v in bar_manager.ta.items():
                partial_bar_manager.ta[k] = v[i: i + size]
            for customized in bar_manager.customized_indicator_name:
                partial_bar_manager.__dict__[customized] = bar_manager.__dict__[customized][i: i + size]
            yield (partial_bar_manager.time[-1], partial_bar_manager)

    def initial_bar_manager_generators(self):
        """
        initial generators
        and save in self.state_generators[sub_types][symbol]
        (dt for bar manager state, bar manager)
        :return:
        """
        for sub_types, symbol_data in self.full_picture_bar_manager.items():
            self.state_generators[sub_types] = dict()
            for symbol, bm in symbol_data.items():
                self.state_generators[sub_types][symbol] \
                    = self.generate_bar_manager_state(bm, self.strategy_lookback_period[symbol][sub_types])

    def update_state(self, dt=None, init=False):
        """

        :param dt:
        :param init:
        :return:
        """
        # generate first state of each ohlc data
        if init is True:
            for kline_type, symbol_generator in self.state_generators.items():  #
                self.state[kline_type] = dict()
                self.bar_timestamp[kline_type] = dict()
                for symbol, generator in symbol_generator.items():
                    bar_t, bar = next(generator)
                    if self.min_timestamp is None or bar_t < self.min_timestamp:
                        self.min_timestamp = bar_t
                    self.state[kline_type][symbol] = bar
                    self.bar_timestamp[kline_type][symbol] = bar_t
                return True
        else:
            # if current dt is less than first dt that bar occupies, skip it
            if dt < self.min_timestamp:
                return False
            for kline_type, symbol_generator in self.state_generators.items():
                for symbol, generator in symbol_generator.items():
                    # this condition is to make sure the unaligned kline input
                    # first generator may generate klines with different starting point with same kline type
                    if dt < self.bar_timestamp[kline_type][symbol]:
                        continue
                    # finish generate if one of the data is finished
                    try:
                        bar_t, bar = next(generator)
                    except StopIteration:
                        return None
                    if bar_t > self.min_timestamp:
                        self.min_timestamp = bar_t
                    self.state[kline_type][symbol] = bar
                    self.bar_timestamp[kline_type][symbol] = bar_t
            return True

    def run(self):
        # self.strategy.load_setting()
        self._initial_strategy()
        self._load_data()
        self._check_data_valid()
        self.strategy.on_strategy_init(datetime.datetime.now())
        self._infer_time()
        self.initial_bar_manager_generators()

        # last_state = self.strategy.lookback_period.copy()
        self.update_state(init=True)
        start = datetime.datetime.now()
        for t in self.time_list:
            # if t is in the smallest timestamp the strategy should make decision
            self.brokerage_ctx.update_time(t)
            if t == self.min_timestamp:
                # todo test that whether can handle same ktype data with different start
                matching_order = True
                for k, on_bar in self.kline_type_on_bar_match.items():
                    if k in self.bar_timestamp.keys():
                        keys = [k for k, v in self.bar_timestamp[k].items() if v == t]
                        bar_state = {k: v for k, v in self.state[k].items() if k in keys}
                        if matching_order is True:
                            dealt_list = self.brokerage_ctx.match_working_order(bar_state)
                            self.strategy.on_order_status_change(dealt_list)
                            matching_order = False
                        on_bar(bar_state)

            updated = self.update_state(t)
            if updated is None:
                print('finish backtest')
                print(datetime.datetime.now() - start)
                break
            if updated is False:
                print('skip kline for look back')
        self.calculate_result()


if __name__ == '__main__':
    # df = pd.read_csv('../hkex_data/HK.800000_2019-02-25 09:30:00_2020-02-21 16:00:00_K_1M_qfq.csv')

    quote = BacktestingQuote()

    broker = BacktestingBrokerage(100000)

    strategy = DoubleMA()
    backtesting_setting = {
        'data_source': 'csv',

        'data': {
            'HK_FUTURE.999010': {
                'K_1M': '/Users/liujunyue/PycharmProjects/ljquant/hkex_data/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'
            }
        },
        'start': '2019-07-01',
        'end': '2020-04-30',
        'time_key': 'time_key'

    }
    # todo one should guarantee lookback period for same kline_type is same.

    strategy_parameter = {
        "lookback_period": {
            "HK_FUTURE.999010": {
                "K_1M": 100
            }
        },
        "subscribe": {
            "HK_FUTURE.999010": [
                "K_1M"
            ]
        },
        "ta_parameters": {
            "HK_FUTURE.999010": {
                "K_1M": {
                    "MA1": {
                        "indicator": "MA",
                        "period": 5
                    },
                    "MA2": {
                        "indicator": "MA",
                        "period": 10,
                        "matype": "MA_Type.SMA",
                        "price_type": "'close'"
                    },
                    "MA3": {
                        "indicator": "MA",
                        "period": 20
                    }
                }

            }
        },
        "traded_code": "HK_FUTURE.999010"
    }

    backtesting = VectorizedBacktesting(quote, broker, strategy, strategy_parameter,
                                        backtesting_setting=backtesting_setting)
    backtesting.run()
    # g = backtesting.generate_bar_manager_state(backtesting.full_picture_bar_manager['HK.999010']['K_1M'], 100)

    traded = pd.DataFrame([order.order_dict() for order in backtesting.dealt_list])
    traded['dealt_qty'] = np.where(traded['order_direction'] == 'LONG', traded['dealt_qty'], -traded['dealt_qty'])
    traded['dealt_inflow'] = - traded['dealt_price'] * traded['dealt_qty']
    traded_grouped = traded.groupby(['code', 'update_time', 'order_direction']).agg(
        {'dealt_outflow': 'sum', 'dealt_qty': 'sum'})
    traded_grouped.reset_index([2], inplace=True)
    traded_grouped.index = traded_grouped.index.set_names(['code', 'time_key'])
    traded_grouped = traded_grouped.groupby(level=[0]).cumsum()
