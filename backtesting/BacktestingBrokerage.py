from bar_manager.BarManager import BarManager
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
        self.order_count = 0
        if initial_position is None:
            self.current_position: dict = dict()
        else:
            self.current_position = initial_position

    def history_order_list_query(self, *args, **kwargs):
        return 1, self.history_order_list

    def history_deal_list_query(self, *args, **kwargs):
        return 1, self.deal_order_list

    def acctradinginfo_query(self, *args, **kwargs):
        return 1, {'account_id': self.account_id, 'cash': self.cash, 'current position': self.current_position}

    def place_order(self, price, qty, code, trd_side, order_type=None, *args, **kwargs):
        """

        :param price:
        :param qty:
        :param code:
        :param trd_side:
        :param order_type:
        :param args:
        :param kwargs:
        :return:
        """
        ret, data = self._check_place_order_validity(code, price, qty, trd_side)
        if ret == 0:
            return 0, data
        self.order_count += 1
        order = Order(code, price, qty, order_type, trd_side, SUBMITTED, order_time=self.time, update_time=self.time,
                      order_identifier=self.order_count)
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
            self.working_order[order_id].update_time = self.time
            self.history_order_list.append(self.working_order[order_id])
            del self.working_order[order_id]
        elif price is not None and qty is not None:
            old_price = self.working_order[order_id].order_price
            self.working_order[order_id].order_price = price
            self.working_order[order_id].update_time = self.time
            old_qty = self.working_order[order_id].qty
            self.working_order[order_id].qty = qty
            self.history_order_list.append(self.working_order[order_id])
            return 1, 'Change order price from {} to {}, and quantity from {} to {}'.format(old_price, price, old_qty,
                                                                                            qty)
        elif price is not None:
            old_price = self.working_order[order_id].order_price
            self.working_order[order_id].order_price = price
            self.working_order[order_id].update_time = self.time
            self.history_order_list.append(self.working_order[order_id])
            return 1, 'Change order price from {} to {}'.format(old_price, price)
        elif qty is not None:
            old_qty = self.working_order[order_id].qty
            self.working_order[order_id].qty = qty
            self.working_order[order_id].update_time = self.time
            self.history_order_list.append(self.working_order[order_id])
            return 1, 'Change order quantity from {} to {}'.format(old_qty, qty)

    def cancel_all_order(self, *args):
        del_list = []
        for order_id, order in self.working_order.items():
            order.order_status = CANCELLED_ALL
            order.update_time = self.time
            del_list.append(order_id)
            self.history_order_list.append(order)
        for order_id in del_list:
            del self.working_order[order_id]
        return 1, None

    def deal_list_query(self, *args, **kwargs):
        return 1, self.deal_order_list

    def update_time(self, time):
        self.time = time

    def order_deal(self, order_id, deal_price, deal_qty):
        order = self.working_order.pop(order_id)
        order.update_time = self.time
        order.deal = True
        order.dealt_avg_price = deal_price
        order.deal_qty = deal_qty
        order.order_status = FILLED_ALL
        self.deal_order_list.append(order)
        removed_code = []
        if order.code in self.current_position.keys():
            pos = self.current_position[order.code]
            if order.order_direction == 'LONG':
                update_qty = pos['qty'] + order.deal_qty
                if update_qty != 0:
                    pos['cost'] = (pos['cost'] * pos['qty'] + order.dealt_avg_price * order.deal_qty) \
                                  / update_qty
                    pos['qty'] = update_qty
                else:
                    removed_code.append(order.code)
                self.cash -= order.dealt_avg_price * order.deal_qty
            else:
                update_qty = pos['qty'] - order.deal_qty
                if update_qty != 0:
                    pos['cost'] = (pos['cost'] * pos['qty'] - order.dealt_avg_price * order.deal_qty) \
                                  / update_qty
                    pos['qty'] = update_qty
                else:
                    removed_code.append(order.code)
                self.cash += order.dealt_avg_price * order.deal_qty
        else:
            if order.order_direction == 'LONG':
                self.current_position[order.code] = {
                    'cost': order.dealt_avg_price,
                    'qty': order.deal_qty,

                }
                self.cash -= order.dealt_avg_price * order.deal_qty
            else:
                self.current_position[order.code] = {
                    'cost': order.dealt_avg_price,
                    'qty': - order.deal_qty,
                }
                self.cash += order.dealt_avg_price * order.deal_qty

    def limit_order_matching(self, order_id, open_price, high_price, low_price):
        order = self.working_order[order_id]
        dealt_list = []
        if order.order_status == 'SUBMITTED' and (order.order_type is None or order.order_type == 'NORMAL'):
            if order.order_direction == 'LONG':
                if order.order_price >= open_price:
                    deal_price = open_price
                    dealt_list.append((order_id, deal_price, order.order_qty))
                    # self.order_deal(order_id, deal_price, order.order_qty)
                elif order.order_price <= high_price:
                    deal_price = order.order_price
                    dealt_list.append((order_id, deal_price, order.order_qty))
            elif order.order_direction == 'SHORT':
                if order.order_price <= open_price:
                    deal_price = open_price
                    dealt_list.append((order_id, deal_price, order.order_qty))
                elif order.order_price >= low_price:
                    deal_price = order.order_price
                    dealt_list.append((order_id, deal_price, order.order_qty))
        return dealt_list

    def match_working_order(self, bar_state):
        dealt_list = []
        dealt_order_list = []
        for order_id, order in self.working_order.items():
            bm = bar_state[order.code]  # type: BarManager
            open_price = bm.open[-1]
            high_price = bm.close[-1]
            low_price = bm.low[-1]
            # limit order matching
            dealt_list.extend(self.limit_order_matching(order_id, open_price, high_price, low_price))
            # todo add stop order logic
            # todo update current position balance price
        for order_id, deal_price, deal_qty in dealt_list:
            dealt_order_list.append(self.working_order[order_id])
            self.order_deal(order_id, deal_price, deal_qty)
        return dealt_order_list

    def _check_place_order_validity(self, code, price, qty, trd_side):
        """
        This implementation doesn't allow naked short.
        :param code:
        :param price:
        :param qty:
        :param trd_side:
        :return:
        """
        if code in self.current_position.keys():
            # check whether you can buy or sell that amount
            if self.current_position[code]['qty'] > 0:
                if trd_side == 'LONG' and self.cash < price * qty:
                    return 0, \
                           'No enough money to open the position. You want to open {}, but have cash {}'.format(
                               price * qty, self.cash)
                elif trd_side == 'SHORT' and self.current_position[code]['qty'] < qty:
                    # larger than currently holding
                    net_short_qty = qty - self.current_position[code]['qty']
                    if self.cash < price * net_short_qty:
                        return 0, \
                               'No enough money to open the position. You want to open {}, but have cash {}'.format(
                                   price * net_short_qty, self.cash)
            else:
                if trd_side == 'SHORT' and self.cash < price * qty:
                    return 0, \
                           'No enough money to open the position. You want to open {}, but have cash {}'.format(
                               price * qty, self.cash)
                elif trd_side == 'LONG' and self.current_position[code]['qty'] < qty:
                    # larger than currently holding
                    net_long_qty = qty - self.current_position[code]['qty']
                    if self.cash < price * net_long_qty:
                        return 0, \
                               'No enough money to open the position. You want to open {}, but have cash {}'.format(
                                   price * net_long_qty, self.cash)
        else:
            if self.cash < price * qty:
                return 0, 'No enough money to open the position'
        return 1, None
