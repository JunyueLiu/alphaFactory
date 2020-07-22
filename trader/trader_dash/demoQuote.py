from gateway.quote_base import QuoteBase


class DemoQuote(QuoteBase):

    def __init__(self, data):
        super().__init__()
        self.data = data

    def subscribe(self, code_list, subtype_list, *args, **kwargs):
        return 0, 'subscribe: {} type: {} success'.format(code_list, subtype_list)

    def unsubscribe(self, code_list, subtype_list, *args, **kwargs):
        return 0, 'unsubscribe: {} type: {} success'.format(code_list, subtype_list)





