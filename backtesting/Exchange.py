import datetime
import pandas as pd

class Broker:

    def __init__(self, fix_fee: int = 0, variable_fee: float = 0.0, slippage: float = 0.0, leverage: int = 1):
        self.fix_fee = fix_fee
        self.variable_fee = variable_fee
        self.slippage = slippage
        self.leverage = leverage
        self.short_constraints = True
        self.financing = False

        self.name = 'Exchange tabular'
        self.products = []
        self.trade_ids = []
        self.history_order = []
        self.live_order = []
        self.data = None
        self.clock = datetime.datetime.fromtimestamp(0)

    def load_data(self, data):
        self.data = data

    def market_snapshot(self, time):
        pass

    def open_position(self, code, direction, size):
        pass

    def close_position(self, trade_id):
        pass

    def place_order(self, code, direction, size):
        pass

    def cancel_order(self, order_id):
        pass

    def close_all(self):
        pass

    def position_check(self):
        pass

    def update_time(self, timedelta):
        self.clock += timedelta

    def get_trades(self):
        return self.trade_ids

    def load_trades(self, trade_ids):
        self.trade_ids = trade_ids

    def set_fee(self, fee):
        self.fix_fee = fee

    def set_variable_fee(self, fee_rate):
        self.variable_fee = fee_rate

    def set_slippage(self, slippage):
        self.slippage = slippage

if __name__ == '__main__':
    broker = Broker()
    df = pd.read_csv('../hkex_data/HK.800000_2019-02-25 09:30:00_2020-02-21 16:00:00_K_1M_qfq.csv')
    broker.load_data(df)