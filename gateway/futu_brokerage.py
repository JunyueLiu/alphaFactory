from futu import *
from gateway.brokerage_base import BrokerageBase


class FutuBrokerage(BrokerageBase):
    name = 'futu'

    # exchange_name =

    def __init__(self, host="127.0.0.1", port=11111, is_encrypt=None):
        super(BrokerageBase, self).__init__()
        self.context = OpenHKTradeContext(host, port, is_encrypt)  # type: OpenHKTradeContext

    def place_order(self, price, qty, code, trd_side, order_type=None, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0,
                    acc_index=0, remark=None):
        ret, data = self.context.place_order(price, qty, code, trd_side, order_type, adjust_limit=adjust_limit,
                                             trd_env=trd_env, acc_id=acc_id, acc_index=acc_index, remark=remark)
        return ret, data

    def modify_order(self, modify_order_op, order_id, qty, price, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0,
                     acc_index=0):
        ret, data = self.context.modify_order(modify_order_op, order_id, qty, price, adjust_limit=adjust_limit,
                                              trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)
        return ret, data

    def cancel_all_order(self, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0):
        ret, data = self.context.cancel_all_order(trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)
        return ret, data

    def change_order(self, order_id, price, qty, adjust_limit=0, trd_env=TrdEnv.REAL, acc_id=0, acc_index=0):
        ret, data = self.context.change_order(order_id, price, qty, adjust_limit=adjust_limit, trd_env=trd_env,
                                              acc_id=acc_id)
        return ret, data

    def deal_list_query(self, code="", trd_env=TrdEnv.REAL, acc_id=0, acc_index=0, refresh_cache=False):
        ret, data = self.context.deal_list_query(code=code, trd_env=trd_env, acc_id=acc_id, acc_index=acc_index,
                                                 refresh_cache=refresh_cache)
        return ret, data

    def history_order_list_query(self, status_filter_list=[], code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0,
                                 acc_index=0):
        ret, data = self.context.history_order_list_query(status_filter_list=status_filter_list, code=code, start=start,
                                                          end=end, trd_env=trd_env, acc_id=acc_id, acc_index=acc_index)
        return ret, data

    def history_deal_list_query(self, code='', start='', end='', trd_env=TrdEnv.REAL, acc_id=0, acc_index=0):
        ret, data = self.context.history_deal_list_query(code=code, start=start, end=end, trd_env=trd_env,
                                                         acc_id=acc_id, acc_index=acc_index)
        return ret, data

    def acctradinginfo_query(self, order_type, code, price, order_id=None, adjust_limit=0, trd_env=TrdEnv.REAL,
                             acc_id=0, acc_index=0):
        ret, data = self.context.acctradinginfo_query(order_type=order_type, code=code, price=price, order_id=order_id,
                                                      adjust_limit=adjust_limit, trd_env=trd_env, acc_id=acc_id,
                                                      acc_index=acc_index)
        return ret, data

    def set_handler(self, handler):
        ret = self.context.set_handler(handler)
        return ret
