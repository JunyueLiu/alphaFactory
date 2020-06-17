import datetime as dt

NONE = "N/A"  # 未知状态
UNSUBMITTED = "UNSUBMITTED"  # 未提交
WAITING_SUBMIT = "WAITING_SUBMIT"  # 等待提交
SUBMITTING = "SUBMITTING"  # 提交中
SUBMIT_FAILED = "SUBMIT_FAILED"  # 提交失败，下单失败
TIMEOUT = "TIMEOUT"  # 处理超时，结果未知
SUBMITTED = "SUBMITTED"  # 已提交，等待成交
FILLED_PART = "FILLED_PART"  # 部分成交
FILLED_ALL = "FILLED_ALL"  # 全部已成
CANCELLING_PART = "CANCELLING_PART"  # 正在撤单_部分(部分已成交，正在撤销剩余部分)
CANCELLING_ALL = "CANCELLING_ALL"  # 正在撤单_全部
CANCELLED_PART = "CANCELLED_PART"  # 部分成交，剩余部分已撤单
CANCELLED_ALL = "CANCELLED_ALL"  # 全部已撤单，无成交
FAILED = "FAILED"  # 下单失败，服务拒绝
DISABLED = "DISABLED"  # 已失效
DELETED = "DELETED"  # 已删除，无成交的订单才能删除


class Order:
    def __init__(self, code, order_price, qty, order_type, order_direction, order_status, order_time=None,
                 update_time=None):
        self.code = code
        self.order_time = order_time
        self.order_price = order_price
        self.order_qty = qty
        self.order_type = order_type
        self.order_direction = order_direction
        self.update_time = update_time
        self.deal = False
        self.order_status = order_status
        self.order_id = '{}-{}'.format(self.code, self.order_time)
        self.exchange_order_id = None
        self.deal_qty = 0
        self.dealt_avg_price = 0

    def set_exchange_order_id(self, id):
        self.exchange_order_id = id

    def get_order_id(self):
        return self.order_id

    def get_order_status(self):
        return self.order_status

    def update_order_status(self, update_time, order_status):
        self.update_time = update_time
        self.order_status = order_status

    def set_deal_qty(self, deal_qty):
        self.deal_qty = deal_qty

    def order_dict(self):
        d = {'code': self.code,
             'order_time': self.order_time,
             'order_price': self.order_price,
             'order_qty': self.order_qty,
             'order_type': self.order_type,
             'order_status': self.order_status,
             'update_time': self.update_time,
             'exchange_order_id': self.exchange_order_id,
             'order_id': self.order_id,

             }
        return d


class WarrantOrder(Order):
    def __init__(self, code, order_price, qty, order_type, order_direction, order_status, owner_price, order_time=None,
                 update_time=None):
        super(WarrantOrder, self).__init__(code, order_price, qty, order_type, order_direction, order_status,
                                           order_time,
                                           update_time)
        self.owner_price = owner_price

    def order_dict(self):
        d = super(WarrantOrder, self).order_dict()
        d['owner_price'] = self.owner_price
        return d
