from futu import *

from gateway.quote_base import QuoteBase
import pandas as pd


class FutuQuote(QuoteBase):
    name = 'futu'

    # exchange_name =

    def __init__(self, host, port):
        super(FutuQuote, self).__init__()
        self.context = OpenQuoteContext(host, port)

    def get_history_kline(self, symbol, start=None, end=None, num=1000, ktype=KLType.K_DAY, autype=AuType.QFQ,
                          max_count=1000, page_req_key=None) -> pd.DataFrame:
        if start is None and end is None and num is not None:
            ret, data = self.context.request_history_kline(symbol, start, end, ktype, autype, max_count=1000,
                                                           page_req_key=None)

        return data

    def subscribe(self, code_list, subtype_list, is_first_push=True, subscribe_push=True):

        ret, data  = self.context.subscribe(code_list, subtype_list, is_first_push=is_first_push, subscribe_push=subscribe_push)
        return ret, data

    def unsubscribe(self, code_list, subtype_list, *args, **kwargs):
        pass


