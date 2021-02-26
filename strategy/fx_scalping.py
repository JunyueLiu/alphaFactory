import pandas as pd
import numpy as np

from backtesting.VectorizationBacktesting import VectorizedBacktesting
from backtesting.BacktestingBrokerage import BacktestingBrokerage
from backtesting.BacktestingQuote import BacktestingQuote
from db_wrapper.mongodb_utils import MongoConnection
from order.Order import Order
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class FXScalping(Strategy):

    def __init__(self):
        super(FXScalping, self).__init__()
        self.strategy_name = 'Technical scalping'
        self.author = 'ljy'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'Multi timeframe scalping'
        self.long_only = None
        self.position = 0
        self.traded_code = None
        self.order_sent = False

    def strategy_logic(self, bar: BarManager):
        self.cancel_all()
        price = bar.close[-1]
        if bar.ta['MA1'][-1] >= bar.ta['MA2'][-1] \
                and bar.ta['MA1'][-2] < bar.ta['MA2'][-2]:
            if self.position < 0:
                self.cover(self.traded_code, 1.01 * price, 1, None)
                self.buy(self.traded_code, 1.01 * price, 1, None)
            elif self.position == 0:
                self.buy(self.traded_code, 1.01 * price, 1, None)
        elif bar.ta['MA1'][-1] <= bar.ta['MA2'][-1] \
                and bar.ta['MA1'][-2] > bar.ta['MA2'][-2]:
            if self.position > 0:
                self.sell(self.traded_code, 0.99 * price, 1, None)
                self.short(self.traded_code, 0.99 * price, 1, None)
            elif self.position == 0:
                self.short(self.traded_code, 0.99 * price, 1, None)

    def on_5min_bar(self, bar):
        if self.long_only is None:
            return

        if self.long_only is True:
            if self.order_sent is True:
                return

            m_bar = bar[self.traded_code]
            low = m_bar.low
            high = m_bar.high
            ema_short = m_bar.ta['ema3']
            ema_long = m_bar.ta['ema4']

            if ema_long < low[-1] < ema_short:
                stop_order_price = np.max(high[-5:])

                




        else:
            if self.order_sent is True:
                return

    def on_60min_bar(self, bar):
        h_bar = bar[self.traded_code]
        high = h_bar.high[-1]
        low = h_bar.low[-1]
        ema_short = h_bar.ta['ema1']
        ema_long = h_bar.ta['ema2']
        self.cancel_all()
        # long condition
        if ema_long[-1] < ema_short[-1] < low[-1] \
                and ema_short[-2] <= ema_short[-1]:
            # long condition
            self.long_only = True
        elif ema_long[-1] > ema_short[-1] > high[-1] \
                and ema_short[-2] >= ema_short[-1]:
            # short condition
            self.long_only = False
        else:
            # no scalping
            self.long_only = None

    def on_order_status_change(self, dealt_list: list):
        self.write_log_info('Order change, deal: {}'.format(dealt_list))
        if len(dealt_list) > 0:
            for order in dealt_list:
                if order.order_direction == "LONG":
                    self.position += 1
                else:
                    self.position -= 1
