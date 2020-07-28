import json
import pandas as pd
from futu import CurKlineHandlerBase, RET_OK, TradeOrderHandlerBase, TradeDealHandlerBase

from gateway.brokerage_base import BrokerageBase
from gateway.futu_brokerage import FutuBrokerage
from gateway.futu_quote import FutuQuote
from gateway.quote_base import QuoteBase
from strategy.StrategyBase import Strategy


class TraderBase:
    def __init__(self, quote: QuoteBase, brokerage: BrokerageBase, strategy: Strategy, strategy_parameter):

        self.quote_ctx = quote
        self.brokerage_ctx = brokerage
        self.strategy = strategy
        self.trade_setting = None
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


class FutuTrader(TraderBase):
    def __init__(self, quote: FutuQuote, brokerage: FutuBrokerage, strategy: Strategy, strategy_parameter):
        super().__init__(quote, brokerage, strategy, strategy_parameter)


    def run(self):
        self._initial_strategy()

        class CurKline(CurKlineHandlerBase):
            strategy = self.strategy

            def on_recv_rsp(self, rsp_pb):
                ret_code, data = super(self.__class__, self).on_recv_rsp(rsp_pb)
                if ret_code != RET_OK:
                    print('CurKline: %s' % data)
                    return ret_code, data

                data['time_key'] = pd.to_datetime(data['time_key'])
                data.set_index('time_key', inplace=True)
                self.strategy.process_kline(data)
                return ret_code, data

        class TradeOrder(TradeOrderHandlerBase):
            strategy = self.strategy

            def on_recv_rsp(self, rsp_pb):
                # col_list = ['trd_env', 'code', 'stock_name', 'dealt_avg_price', 'dealt_qty',
                #             'qty', 'order_id', 'order_type', 'price', 'order_status',
                #             'create_time', 'updated_time', 'trd_side', 'last_err_msg', 'trd_market', "remark"
                #             ]
                ret, data = super(TradeOrder, self).on_recv_rsp(rsp_pb)
                if ret == RET_OK:
                    self.strategy.on_order_send(data)
                else:
                    self.strategy.write_log_error('trade order error: {}'.format(data))

        class TradeDeal(TradeDealHandlerBase):
            strategy = self.strategy

            def on_recv_rsp(self, rsp_pb):
                # ['trd_env', 'code', 'stock_name', 'deal_id', 'order_id',
                #  'qty', 'price', 'trd_side', 'create_time', 'counter_broker_id',
                #  'counter_broker_name', 'trd_market', 'status'
                #  ]
                ret, content = super(TradeDeal, self).on_recv_rsp(rsp_pb)
                if ret == RET_OK:
                    self.strategy.on_order_status_change(content)
                else:
                    self.strategy.write_log_error('trade deal error: {}'.format(content))



        handler = CurKline()
        trade_handler = TradeOrder()
        deal_handler = TradeDeal()
        self.quote_ctx.set_handler(handler)
        self.brokerage_ctx.set_handler(trade_handler)
        self.brokerage_ctx.set_handler(deal_handler)
