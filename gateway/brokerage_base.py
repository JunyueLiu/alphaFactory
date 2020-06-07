class BrokerageBase:
    name = ''
    exchange_name = ''

    def __init__(self):
        pass

    def place_order(self, price, qty, code, trd_side, order_type=None, *args, **kwargs):
        pass

    def modify_order(self, modify_order_op, order_id, qty, price, *args, **kwargs):
        pass

    def cancel_all_order(self, *args):
        pass

    def change_order(self, order_id, price, qty, *args, **kwargs):
        pass

    def deal_list_query(self, *args, **kwargs):
        pass

    def history_order_list_query(self, *args, **kwargs):
        pass

    def history_deal_list_query(self, *args, **kwargs):
        pass

    def acctradinginfo_query(self, *args, **kwargs):
        pass

    def set_handler(self, handler):
        pass

