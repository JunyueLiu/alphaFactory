from bar_manager.BarManager import BarManager
from strategy.StrategyBase import Strategy


class TWAP(Strategy):

    def __init__(self):
        super(TWAP, self).__init__()
        self.strategy_name = 'TWAP'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'TWAP algo trading'
        self.position = 0
        self.traded_code = None

    def strategy_logic(self, bar: BarManager):
        pass

    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])

    def on_order_status_change(self, *args, **kwargs):
        pass


class VWAP(Strategy):

    def __init__(self):
        super(VWAP, self).__init__()
        self.strategy_name = 'VWAP'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'VWAP algo trading'
        self.position = 0
        self.traded_code = None

    def strategy_logic(self, bar: BarManager):
        pass

    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])

    def on_order_status_change(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    strategy_parameter = {
        "lookback_period": {
            "HK_FUTURE.999010": {
                "K_1M": 1000
            }
        },
        "subscribe": {
            "HK_FUTURE.999010": [
                "K_1M"
            ]
        },
        # "ta_parameters": {}
        "traded_code": "HK_FUTURE.999010"
    }