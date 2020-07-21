import json
import pickle
import datetime
import pandas as pd
import numpy as np
from tqdm import tqdm

from backtesting.Backtesting import BacktestingBase
from backtesting.dash_app.index_app import get_backtesting_report_dash_app
from db_wrapper.mongodb_utils import MongoConnection

from gateway.quote_base import QuoteBase
from gateway.brokerage_base import BrokerageBase
from backtesting.BacktestingQuote import BacktestingQuote
from backtesting.BacktestingBrokerage import BacktestingBrokerage
from backtesting.backtesting_metric import *
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager



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
                if isinstance(v, list):
                    ll = []
                    for t in v:
                        ll.append(t[i: i + size])
                    partial_bar_manager.ta[k] = ll
                else:
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
        self._load_setting(self.backtesting_setting)
        self._initial_strategy()
        self._load_data()
        self._check_data_valid()
        self.strategy.on_strategy_init(datetime.datetime.now())
        self._infer_time()
        self.initial_bar_manager_generators()

        # last_state = self.strategy.lookback_period.copy()
        self.update_state(init=True)
        start = datetime.datetime.now()
        for t in tqdm(self.time_list):
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
                pass
                # print('skip kline for look back')
        self.calculate_result()