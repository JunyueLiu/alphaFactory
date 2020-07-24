from gateway.brokerage_base import BrokerageBase
from gateway.quote_base import QuoteBase
from strategy.StrategyBase import Strategy


class TraderBase:
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter):

        self.quote_ctx = quote
        self.brokerage_ctx = brokerage
        self.strategy = strategy
        self.strategy_parameter = strategy_parameter

