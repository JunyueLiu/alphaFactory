import pandas as pd

from order.Order import Order
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class DoubleMA(Strategy):

    def __init__(self):
        super(DoubleMA, self).__init__()
        self.strategy_name = 'Double MA Strategy'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'Two MA lines, cross over'
        self.position = 0
        self.traded_code = None

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


    def process_kline(self, data: pd.DataFrame):
        super(DoubleMA, self).process_kline(data)

    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])


    def on_order_status_change(self, dealt_list: list):
        if len(dealt_list) > 0:
            for order in dealt_list:
                if order.order_direction == "LONG":
                    self.position += 1
                else:
                    self.position -= 1
