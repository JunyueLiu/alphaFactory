from gateway.brokerage_base import BrokerageBase
from order.Order import *
import datetime


class BacktestingBrokerage(BrokerageBase):
    def __init__(self, initial_cash=100, initial_position=None, account_id=None):
        super().__init__()
        self.cash = initial_cash
        self.history_order_list = []
        self.deal_order_list = []
        self.working_order = {}
        self.account_id = account_id
        self.time = None
        if initial_position is None:
            self.current_position = []
        else:
            self.current_position = initial_position

    def history_order_list_query(self, *args, **kwargs):
        return 1, self.history_order_list

    def history_deal_list_query(self, *args, **kwargs):
        return 1, self.deal_order_list

    def acctradinginfo_query(self, *args, **kwargs):
        return 1, {'account_id': self.account_id, 'cash': self.cash, 'current position': self.current_position}

    def place_order(self, price, qty, code, trd_side, order_type=None, *args, **kwargs):
        order = Order(code, price, qty, order_type, trd_side, SUBMITTED, order_time=self.time, update_time=self.time)
        self.working_order[order.order_id] = order
        self.history_order_list.append(order)
        return 1, None

    def modify_order(self, modify_order_op, order_id, qty, price, *args, **kwargs):
        # super().modify_order(modify_order_op, order_id, qty, price, *args, **kwargs)
        pass

    def change_order(self, order_id, price=None, qty=None, order_status=None, *args, **kwargs):
        if order_id not in self.working_order.keys():
            return 0, 'The order is dealt or canceled.'

        if order_status == 'CANCEL':
            self.working_order[order_id].order_status = CANCELLED_ALL
            self.history_order_list.append(self.working_order[order_id])
            del self.working_order[order_id]
        elif price is not None and qty is not None:
            old_price = self.working_order[order_id].order_price
            self.working_order[order_id].order_price = price
            old_qty = self.working_order[order_id].qty
            self.working_order[order_id].qty = qty
            self.history_order_list.append(self.working_order[order_id])
            return 1, 'Change order price from {} to {}, and quantity from {} to {}'.format(old_price, price, old_qty,
                                                                                            qty)
        elif price is not None:
            old_price = self.working_order[order_id].order_price
            self.working_order[order_id].order_price = price
            self.history_order_list.append(self.working_order[order_id])
            return 1, 'Change order price from {} to {}'.format(old_price, price)
        elif qty is not None:
            old_qty = self.working_order[order_id].qty
            self.working_order[order_id].qty = qty
            self.history_order_list.append(self.working_order[order_id])
            return 1, 'Change order quantity from {} to {}'.format(old_qty, qty)

    def cancel_all_order(self, *args):
        del_list = []
        for order_id, order in self.working_order.items():
            order.order_status = CANCELLED_ALL
            del_list.append(order_id)
            self.history_order_list.append(order)
        for order_id in del_list:
            del self.working_order[order_id]
        return 1, None

    def deal_list_query(self, *args, **kwargs):
        return 1, self.deal_order_list


    def _update_time(self, time):
        self.time = time

    def order_deal(self, order_id):
        order = self.working_order.pop(order_id)
        order.order_status = FILLED_ALL
        self.history_order_list.append(order)

