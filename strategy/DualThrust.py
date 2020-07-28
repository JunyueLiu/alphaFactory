import pandas as pd

from backtesting.VectorizationBacktesting import VectorizedBacktesting
from backtesting.BacktestingBrokerage import BacktestingBrokerage
from backtesting.BacktestingQuote import BacktestingQuote
from order.Order import Order
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class DualThrust(Strategy):

    def __init__(self):
        super(DualThrust, self).__init__()
        self.strategy_name = 'DualThrust Strategy'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = ''
        self.position = 0
        self.traded_code = None

    def strategy_logic(self, bar: BarManager):
        self.cancel_all()
        price = bar.close[-1]
        if price >= bar.ta['DUAL'][0][-1]:
            if self.position < 0:
                self.cover(self.traded_code, 1.01 * price, 1, None)
                self.buy(self.traded_code, 1.01 * price, 1, None)
            elif self.position == 0:
                self.buy(self.traded_code, 1.01 * price, 1, None)
        elif price <= bar.ta['DUAL'][1][-1]:
            if self.position > 0:
                self.sell(self.traded_code, 0.99 * price, 1, None)
                self.short(self.traded_code, 0.99 * price, 1, None)
            elif self.position == 0:
                self.short(self.traded_code, 0.99 * price, 1, None)


    def process_kline(self, data: pd.DataFrame):
        super(DualThrust, self).process_kline(data)

    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])


    def on_order_status_change(self, dealt_list: list):
        self.write_log_info('Order change, deal: {}'.format(dealt_list))
        if len(dealt_list) > 0:
            for order in dealt_list:
                if order.order_direction == "LONG":
                    self.position += 1
                else:
                    self.position -= 1

if __name__ == '__main__':
    quote = BacktestingQuote()
    broker = BacktestingBrokerage()
    strategy = DualThrust()
    backtesting_setting = {
        'initial_capital': 100000,
        'data_source': 'csv',

        'data': {
            'HK_FUTURE.999010': {
                'K_1M': r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'
            }
        },
        'benchmark': r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv',
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
                    "DUAL": {
                        "indicator": "DUALTHRUST",
                        "period": 50,
                        "k1": 0.5,
                        "k2": 0.5
                    },
                }

            }
        },
        "traded_code": "HK_FUTURE.999010"
    }

    backtesting = VectorizedBacktesting(quote, broker, strategy, strategy_parameter,
                                        backtesting_setting=backtesting_setting)

    backtesting.run()
    # backtesting.backtesting_result_save_pickle(strategy.strategy_name + '_' + strategy.strategy_version + '_1.pickle')
    backtesting.get_dash_report().run_server('127.0.0.1',)