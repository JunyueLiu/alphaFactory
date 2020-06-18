from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class DoubleMA(Strategy):

    def __init__(self):
        super(DoubleMA, self).__init__()
        self.strategy_name = 'Double MA Strategy'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'Two MA lines, cross over'

    def strategy_logic(self, bar: BarManager):
        print(bar.__dict__)
        if bar.ta['MA1'][-1] > bar.ta['MA2'][-1] and bar.ta['MA1'][-2] < bar.ta['MA2'][-2]:
            print('cross buy')
        else:
            print('no')

    def process_kline(self, data):
        for ix, row in data.iterrows():
            code = row['code']
            if row['k_type'] == 'K_1M':
                if self.last_bar['K_1M'] < ix:  # new bar comes in
                    self.same_bar_traded = False
                    self.on_1min_bar(self.k_1m)
                    # self.strategy_logic(self.k_1m)
                    self.last_bar['K_1M'] = ix
                    self.k_1m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_1m[code].update_with_pandas(row, time_key='time_key')
                    self.on_1min_bar(self.k_1m)
            self.logger.info('process_kline for {} {}'.format(ix, code))

    def on_1min_bar(self, bar: dict):
        print('on_1_min')
        if bar.ta['MA1'][-1] > bar['HK.999010'].ta['MA2'][-1] \
                and bar['HK.999010'].ta['MA1'][-2] < bar['HK.999010'].ta['MA2'][-2]:
            pass
        self.strategy_logic()

    def buy(self, symbol, price, vol, order_type, *args, **kwargs):
        pass

    def sell(self, symbol, price, vol, order_type, *args, **kwargs):
        pass

    def short(self, symbol, price, vol, order_type, *args, **kwargs):
        pass

    def cover(self, symbol, price, vol, order_type, *args, **kwargs):
        pass

    def run_strategy(self):
        pass
