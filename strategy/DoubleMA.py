import pandas as pd
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class DoubleMA(Strategy):

    def __init__(self):
        super(DoubleMA, self).__init__()
        self.strategy_name = 'Double MA Strategy'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'Two MA lines, cross over'
        self.long = None
        self.traded_code = None

    def strategy_logic(self, bar: BarManager):
        # print(bar.__dict__)
        self.cancel_all()

        price = bar.close[-1]
        if bar.ta['MA1'][-1] >= bar.ta['MA2'][-1] \
                and bar.ta['MA1'][-2] < bar.ta['MA2'][-2]:
            if self.long is False:
                self.cover(self.traded_code, price, 1, None)
            self.long = True
            self.buy(self.traded_code, price, 1, None)
        elif bar.ta['MA1'][-1] <= bar.ta['MA2'][-1] \
                and bar.ta['MA1'][-2] > bar.ta['MA2'][-2]:
            if self.long is True:
                self.sell(self.traded_code, price, 1, None)
            self.short(self.traded_code, price, 1, None)
            self.long = False

    def process_kline(self, data: pd.DataFrame):
        super(DoubleMA, self).process_kline(data)

    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])

    def run_strategy(self):
        pass
