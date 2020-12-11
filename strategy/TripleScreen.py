import pandas as pd

from backtesting.VectorizationBacktesting import VectorizedBacktesting
from backtesting.BacktestingBrokerage import BacktestingBrokerage
from backtesting.BacktestingQuote import BacktestingQuote
from strategy.StrategyBase import Strategy
from bar_manager.BarManager import BarManager


class TripleScreen(Strategy):

    def __init__(self):
        super(TripleScreen, self).__init__()
        self.strategy_name = 'Triple Screen Strategy'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'Triple Screen from trading for living'
        self.position = 0
        self.traded_code = None
        self.long_term_trend = None
        self.short_term_reversal = None



    def strategy_logic(self, bar: BarManager):
        self.cancel_all()
        price = bar.close[-1]
        if bar.ta['MA1'][-1] >= bar.ta['MA2'][-1] \
                and bar.ta['MA1'][-2] < bar.ta['MA2'][-2]:
            if self.position < 0:
                self.cover(self.traded_code, 1.01 * price, 200, None)
                # self.buy(self.traded_code, 1.01 * price, 1, None)
            elif self.position == 0:
                if self.long_term_trend is True and self.short_term_reversal is True:
                    self.buy(self.traded_code, 1.01 * price, 200, None)
        elif bar.ta['MA1'][-1] <= bar.ta['MA2'][-1] \
                and bar.ta['MA1'][-2] > bar.ta['MA2'][-2]:
            if self.position > 0:
                self.sell(self.traded_code, 0.99 * price, 200, None)
                # self.short(self.traded_code, 0.99 * price, 1, None)
            elif self.position == 0:
                if self.long_term_trend is False and self.short_term_reversal is False:
                    self.short(self.traded_code, 0.99 * price, 200, None)

    def on_60min_bar(self, bar: dict):
        bm = bar[self.traded_code] # type: BarManager
        if bm.ta['MACD'][2][-1] > 0 and bm.ta['HT_TRENDLINE'][-1] < bm.close[-1]:
            self.long_term_trend = True
        elif bm.ta['MACD'][2][-1] < 0 and bm.ta['HT_TRENDLINE'][-1] > bm.close[-1]:
            self.long_term_trend = False
        else:
            self.long_term_trend = None
        # print(bar[self.traded_code].ta['MACD'])

    def on_15min_bar(self, bar: dict):
        bm = bar[self.traded_code]  # type: BarManager
        if bm.ta['RSI'][-1] <= 20:
            self.short_term_reversal = True
        elif bm.ta['RSI'][-1] >= 80:
            self.short_term_reversal = False
        else:
            self.short_term_reversal = None


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
    strategy = TripleScreen()
    backtesting_setting = {
        'initial_capital': 100000,
        'data_source': 'csv',

        'data': {
            'HK.01810': {
                'K_1M': r'../local_data/HK.01810_2019-12-09 09:30:00_2020-12-08 16:00:00_K_1M_qfq.csv',
                'K_15M': r'../local_data/HK.01810_2019-12-09 09:45:00_2020-12-08 16:00:00_K_15M_qfq.csv',
                'K_60M': r'../local_data/HK.01810_2019-12-09 10:30:00_2020-12-08 16:00:00_K_60M_qfq.csv',
            }
        },
        # 'benchmark': r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv',
        'start': '2020-01-01',
        'end': '2020-11-30',
        'time_key': 'time_key'

    }
    # todo one should guarantee lookback period for same kline_type is same.

    strategy_parameter = {
        "lookback_period": {
            "HK.01810": {
                "K_1M": 20,
                "K_15M": 14,
                "K_60M": 26
            }
        },
        "subscribe": {
            "HK.01810": [
                "K_1M", "K_15M", "K_60M"
            ]
        },
        "ta_parameters": {
            "HK.01810": {
                "K_1M": {
                    "MA1": {
                        "indicator": "MA",
                        "period": 10
                    },
                    "MA2": {
                        "indicator": "MA",
                        "period": 20,
                        "matype": "MA_Type.SMA",
                        "price_type": "'close'"
                    },
                },
                "K_15M": {
                    "RSI":{
                        "indicator": "RSI",
                        "period": 10,


                    }

                },
                "K_60M": {
                    "MACD": {
                        "indicator": "MACD",

                    },
                    "HT_TRENDLINE": {
                        "indicator": "HT_TRENDLINE",
                        # "overlap": True

                    },

                }

            }
        },
        "traded_code": "HK.01810"
    }

    backtesting = VectorizedBacktesting(quote, broker, strategy, strategy_parameter,
                                        backtesting_setting=backtesting_setting)

    backtesting.run()
    backtesting.get_dash_report().run_server('127.0.0.1', debug=True)