from futu import *

from gateway.quote_base import QuoteBase
import pandas as pd


class FutuQuote(QuoteBase):
    name = 'futu'

    # exchange_name =

    def __init__(self, host, port):
        super(FutuQuote, self).__init__()
        self.context = OpenQuoteContext(host, port) # type: OpenQuoteContext

    #分页查询
    def get_history_kline(self, symbol, start=None, end=None, num=1000, ktype=KLType.K_DAY, autype=AuType.QFQ,
                          max_count=1000, page_req_key=None) -> pd.DataFrame:
        ret, data, page_req_key = self.context.request_history_kline(symbol, start, end, ktype, autype, max_count=max_count,page_req_key=page_req_key)
        return ret, data, page_req_key

    #All records
    # return--->pd.Dataframe
    def get_all_history_kline(self,symbol, start=None, end=None, num=1000, ktype=KLType.K_DAY, autype=AuType.QFQ,
                          max_count=1000, page_req_key=None):
        ret, data, page_req_key = self.context.request_history_kline(symbol, start, end, ktype, autype, max_count=max_count,page_req_key=page_req_key)
        if ret !=  RET_OK:
            raise Exception("NO RECORDS!")
        df_list = []
        df_list.append(data)
        while page_req_key != None:  # 请求后面的所有结果
            ret, data, page_req_key = self.context.request_history_kline(symbol, start, end, ktype, autype, max_count=max_count,page_req_key=page_req_key)  # 请求翻页后的数据
            if ret == RET_OK:
                df_list.append(data)
            else:
                raise Exception("Pageable Request Error")
        df = pd.concat(df_list)
        return df

    def subscribe(self, code_list, subtype_list, is_first_push=True, subscribe_push=True):
        ret, data  = self.context.subscribe(code_list, subtype_list, is_first_push=is_first_push, subscribe_push=subscribe_push)
        return ret, data

    def unsubscribe(self, code_list, subtype_list, unsubscribe_all=False,*args, **kwargs):
        ret,data = self.context.unsubscribe(code_list,subtype_list,unsubscribe_all=unsubscribe_all)
        return ret,data

    def get_trading_date(self, market, start, end, *args, **kwargs):
        ret,data = self.context.get_trading_days(market, start, end)
        return ret,data

    def get_symbol_basic_info(self, market, symbol_type, symbol_list=None, *args, **kwargs):
        ret_code,content = self.context.get_stock_basicinfo(market,symbol_type,symbol_list)
        return ret_code,content

    def get_market_snapshot(self, symbol_list, *args, **kwargs):
        ret,data = self.context.get_market_snapshot(symbol_list)
        return ret,data

    def get_broker_queue(self, symbol, *args, **kwargs):
        # if ret == RET_ERROR bid_frame_table,ask_frame_table will store ERROR MSG
        ret,bid_frame_table,ask_frame_table = self.context.get_broker_queue(symbol)
        return ret,bid_frame_table,ask_frame_table

    def get_rt_data(self, symbol, *args, **kwargs):
        ret,data = self.context.get_rt_data(symbol)
        return ret,data

    def unsubscribe_all(self):
        ret,data = self.context.unsubscribe_all()
        return ret,data

    def query_subscription(self,is_all_conn):
        ret,data = self.context.query_subscription(is_all_conn=is_all_conn)
        return ret,data

    def get_stock_quote(self,code_list):
        ret,data = self.context.get_stock_quote(code_list)
        return ret,data

    def get_cur_kline(self, symbol, num, ktype, autype=AuType.QFQ,*args, **kwargs):
        ret,data = self.context.get_cur_kline(symbol, num, ktype,autype=autype)
        return ret,data

    def get_order_book(self, symbol, num=10,*args, **kwargs):
        ret,data = self.context.get_order_book(symbol,num=num)
        return ret,data

    def set_handler(self, handler):
        self.context.set_handler(handler)


