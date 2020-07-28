class QuoteBase:
    name = ''
    exchange_name = ''

    def __init__(self):
        pass

    def get_trading_date(self, market, start, end, *args, **kwargs):
        pass

    def get_symbol_basic_info(self, market, symbol_type, symbol_list=None, *args, **kwargs):
        pass

    def get_market_snapshot(self, symbol_list, *args, **kwargs):
        pass

    def get_history_kline(self, symbol, start, end, kline_type, num, *args, **kwargs):
        pass

    def get_broker_queue(self, symbol, *args, **kwargs):
        pass

    def get_rt_data(self, symbol, *args, **kwargs):
        pass

    def subscribe(self, code_list, subtype_list, *args, **kwargs):
        pass

    def unsubscribe(self, code_list, subtype_list, *args, **kwargs):
        pass

    def unsubscribe_all(self, *args, **kwargs):
        pass

    def query_subscription(self, *args, **kwargs):
        pass

    def get_stock_quote(self,*args, **kwargs):
        pass

    def get_cur_kline(self, symbol, num, ktype, *args, **kwargs):
        pass

    def get_order_book(self, symbol, *args, **kwargs):
        pass

    def set_handler(self, handler):
        pass