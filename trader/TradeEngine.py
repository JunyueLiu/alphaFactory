import json
from gateway.brokerage_base import BrokerageBase
from gateway.quote_base import QuoteBase
from strategy.StrategyBase import Strategy


class TraderBase:
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter):

        self.quote_ctx = quote
        self.brokerage_ctx = brokerage
        self.strategy = strategy
        self.trade_setting = None # im
        self.strategy_parameter = strategy_parameter


    def _initial_strategy(self):
        """
        To initial strategy, call before run the trade engine
        :return:
        """
        self.strategy.load_setting(self.strategy_parameter)
        self.strategy.set_quote_context(self.quote_ctx)
        self.strategy.set_brokerage_context(self.brokerage_ctx)

    def _load_setting(self, setting: dict or str):
        if isinstance(setting, dict):
            self.trade_setting = setting
        elif isinstance(setting, str):
            with open(setting, 'rb') as f:
                df = f.read()
                f.close()
                self.trade_setting = json.loads(df)
        d = self.__dict__
        for key in d.keys():
            if key in self.trade_setting.keys():
                d[key] = self.trade_setting[key]


    def run(self):
        pass