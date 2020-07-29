from bar_manager.BarManager import BarManager
from strategy.StrategyBase import Strategy


class TWAP(Strategy):

    def __init__(self, pos_goal: int, trade_code: str, min_to_finish: int):
        super(TWAP, self).__init__()
        self.strategy_name = 'TWAP'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'TWAP algo trading'
        self.position = pos_goal
        self.traded_code = trade_code
        self.min = min_to_finish

    def strategy_logic(self, bar: BarManager):
        self.cancel_all()
        price = bar.close[-1]
        self.min -= 1
        if self.min > 0:
            pos_to_trade = int(self.position / self.min)
        else:
            pos_to_trade = self.position
        if self.position > 0:
            self.buy(self.traded_code, price, pos_to_trade, None)
        elif self.position < 0:
            self.sell(self.traded_code, price, pos_to_trade, None)

    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])

    def on_order_status_change(self, dealt_list: list):
        self.write_log_info('Order change, deal: {}'.format(dealt_list))
        if len(dealt_list) > 0:
            for order in dealt_list:
                if order.order_direction == "LONG":
                    self.position -= order.order_qty
                else:
                    self.position += order.order_qty
        if self.position == 0:
            self.write_log_info('All trade finish')


class VWAP(Strategy):

    def __init__(self, pos_goal: int, trade_code: str, vol_percentage: float):
        super(VWAP, self).__init__()
        self.strategy_name = 'VWAP'
        self.author = 'AlphaFactory Trader'
        self.strategy_version = '0.0.1'
        self.strategy_description = 'VWAP algo trading'
        self.position = pos_goal
        self.traded_code = trade_code
        self.vol_percentage = vol_percentage

    def strategy_logic(self, bar: BarManager):
        self.cancel_all()
        price = bar.close[-1]
        volume = bar.volume[-1]
        pos_to_trade = min(int(self.vol_percentage * volume), self.position)
        if self.position > 0:
            self.buy(self.traded_code, price, pos_to_trade, None)
        elif self.position < 0:
            self.sell(self.traded_code, price, pos_to_trade, None)


    def on_1min_bar(self, bar: dict):
        self.strategy_logic(bar[self.traded_code])

    def on_order_status_change(self, dealt_list: list):
        self.write_log_info('Order change, deal: {}'.format(dealt_list))
        if len(dealt_list) > 0:
            for order in dealt_list:
                if order.order_direction == "LONG":
                    self.position -= order.order_qty
                else:
                    self.position += order.order_qty
        if self.position == 0:
            self.write_log_info('All trade finish')


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