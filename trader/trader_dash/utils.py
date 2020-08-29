from futu.quote.quote_get_warrant import Request

from gateway.futu_quote import *
from gateway.futu_brokerage import *





def cbbc_selection(futu_quote: FutuQuote, setting: dict):
    req = Request()
    req.status = WarrantStatus.NORMAL
    req.type_list = setting['type_list']
    req.issuer_list = setting['issuer_list']
    req.price_recovery_ratio_min = setting['price_recovery_ratio_min']
    req.price_recovery_ratio_max = setting['price_recovery_ratio_max']
    req.sort_field = SortField.STREET_RATE
    req.ascend = False
    ret, data = futu_quote.get_warrants(setting['owner'], req)
    return ret, data



if __name__ == '__main__':
    cbbc_bull_setting = {
        'owner': 'HK.800000',
        'type_list': [
          'BULL'
        ],
        'issuer_list': [
            'SG',
        ],
        'price_recovery_ratio_min': 1.5,
        'price_recovery_ratio_max': 3.0,
    }

    cbbc_bear_setting = {
        'owner': 'HK.800000',
        'type_list': [
            'BEAR'
        ],
        'issuer_list': [
            'SG',
        ],
        'price_recovery_ratio_min': -1.5,
        'price_recovery_ratio_max': -3.0,
    }


    futu_quote = FutuQuote()
    ret, data=cbbc_selection(futu_quote, cbbc_setting)

