from strategy.StrategyBase import Strategy


class DoubleMA(Strategy):

    def __init__(self):
        super(DoubleMA, self).__init__()
        self.strategy_name = 'Double MA Strategy'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'Two MA lines, cross over'

    def strategy_logic(self, data):
        pass

    def process_kline(self, data):
        for ix, row in data.iterrows():
            code = row['code']
            if row['k_type'] == 'K_1M':
                if self.last_bar['K_1M'] < ix:  # new bar comes in
                    self.same_bar_traded = False
                    self.strategy_logic(self.k_1m)
                    self.last_bar['K_1M'] = ix
                    self.k_1m[code].update_with_pandas(row, time_key='time_key')
                else:
                    self.k_1m[code].update_with_pandas(row, time_key='time_key')
                    self.strategy_logic(self.k_1m)
            self.logger.info('process_kline for {} {}'.format(ix, code))

    def on_1min_bar(self, bar):
        pass

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
