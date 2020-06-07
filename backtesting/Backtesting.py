import json
import pandas as pd
# from backtesting.Exchange import *
from strategy.StrategyBase import Strategy
from gateway.quote_base import QuoteBase
from gateway.brokerage_base import BrokerageBase
from backtesting.BacktestingQuote import BacktestingQuote
from backtesting.BacktestingBrokerage import BacktestingBrokerage


class BacktestingBase:
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter
                 , start=None, end=None, initial_capital=100, backtesting_setting=None):
        self.quote_ctx = quote
        self.brokerage_ctx = brokerage
        self.strategy = strategy
        self.strategy_parameter = strategy_parameter
        self.start = start
        self.end = end
        self.initial_capital = initial_capital
        self.backtesting_setting = backtesting_setting

        self.data = None
        self.data_source = None

    def _check_data_valid(self):
        """
        Check whether the data provided for backtesting is enough for strategy subscription
        :return:
        """
        for symbol, subtype_data in self.data.items():
            if symbol not in self.strategy_parameter['subscribe'].keys():
                raise ValueError('The data for backtesting doesn\'t include {}', symbol)
            else:
                for s in self.strategy_parameter['subscribe'][symbol]:
                    if s not in subtype_data.keys():
                        raise ValueError('The data for backtesting doesn\'t include {}:{}', symbol, s)

    def _initial_strategy(self):
        """
        To initial strategy, call before run the backtesting
        :return:
        """
        self.strategy.load_setting(self.strategy_parameter)
        self.strategy.set_quote_context(self.quote_ctx)
        self.strategy.set_brokerage_context(self.brokerage_ctx)

    def _load_setting(self, setting: dict or str):
        if isinstance(setting, dict):
            self.backtesting_setting = setting
        elif isinstance(setting, str):
            with open(setting, 'rb') as f:
                df = f.read()
                f.close()
                self.backtesting_setting = json.loads(df)
        d = self.__dict__
        for key in d.keys():
            if key in self.backtesting_setting.keys():
                d[key] = self.backtesting_setting[key]

    def _load_data(self):
        pass

    def _reset_data(self):
        self.data = None

    def get_trading_history(self):
        return self.brokerage_ctx.history_order_list_query()

    def _load_data_from_db(self):
        pass

    def _load_data_from_csv(self):
        pass

    def calculate_result(self):
        pass

    def run(self):
        pass


class DayTradeBacktesting(BacktestingBase):
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter):
        super(DayTradeBacktesting, self).__init__(quote, brokerage, strategy, strategy_parameter)


class VectorizedBacktesting(BacktestingBase):
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter):
        super(VectorizedBacktesting, self).__init__(quote, brokerage, strategy, strategy_parameter)

    def _load_data(self):
        pass

    def _initial_strategy(self):
        super()._initial_strategy()

    def _check_data_valid(self):
        super()._check_data_valid()

    def _change_lookback_period(self):
        """
        modify the lookback period to calculate the indicator only once
        :return:
        """
        lookback_period = {}
        for symbol, subtype_data in self.data.items():
            lookback_period[symbol] = {}
            for subtype, data in subtype_data.items():
                lookback_period[symbol][subtype] = len(data)
        self.strategy.strategy_parameters['lookback_period'] = lookback_period

    def run(self):
        # self.strategy.load_setting()
        # overload the lookback to change the performance of barmanager
        self._initial_strategy()
        self._load_data()
        self._check_data_valid()
        self._change_lookback_period()
        self.strategy.init_kline_object()
        # self


if __name__ == '__main__':
    df = pd.read_csv('../hkex_data/HK.800000_2019-02-25 09:30:00_2020-02-21 16:00:00_K_1M_qfq.csv')

    quote = BacktestingQuote()

    broker = BacktestingBrokerage(1)

    strategy = Strategy()
    backtesting_setting = {
        'data_source': 'csv',

        'data': {
            'HK.999010': {
                'K_1M': '/Users/liujunyue/PycharmProjects/ljquant/hkex_data/HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'
            }
        },
        'start': '2019-07-01',
        'end': '2020-05-30',

    }

    backtesting = VectorizedBacktesting(quote, broker, strategy,
                                        '/Users/liujunyue/PycharmProjects/ljquant/strategy/1_min_hsi_futures_setting.json')
    backtesting.run()
