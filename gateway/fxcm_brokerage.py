import fxcmpy

from gateway.brokerage_base import BrokerageBase


class FxcmBrokerage(BrokerageBase):
    name = 'fxcm'

    def __init__(self, fxcm=None, access_token='', config_file='',
                 log_file=None, log_level='', server='demo',
                 proxy_url=None, proxy_port=None, proxy_type=None):
        super(FxcmBrokerage, self).__init__()
        if fxcm is None:
            self.con = fxcmpy.fxcmpy(access_token=access_token, config_file=config_file,
                                     log_file=log_file, log_level=log_level, server=server,
                                     proxy_url=proxy_url, proxy_port=proxy_port, proxy_type=proxy_type)
        else:
            self.con = fxcm  # type: fxcmpy.fxcmpy

    def place_order(self, price, qty, code, trd_side, order_type='AtMarket', time_in_force='GTC', rate=0,
                    is_in_pips=True, limit=None, at_market=0, stop=None,
                    trailing_step=None, account_id=None, close_id=None, *args, **kwargs):
        # GTC – Good Till Cancelled
        # IOC – Immediate Or Cancel
        # FOK – Fill Or Kill
        # DAY – Day Order
        # GTD – Good Till Date
        try:
            if trd_side == 'BUY':
                self.con.open_trade(symbol=code, is_buy=True, amount=qty, time_in_force=time_in_force,
                                    order_type=order_type, rate=rate, is_in_pips=is_in_pips, limit=limit,
                                    at_market=at_market,
                                    stop=stop, trailing_step=trailing_step, account_id=account_id)
            elif trd_side == 'SHORT':
                self.con.open_trade(symbol=code, is_buy=False, amount=qty, time_in_force=time_in_force,
                                    order_type=order_type, rate=rate, is_in_pips=is_in_pips, limit=limit,
                                    at_market=at_market,
                                    stop=stop, trailing_step=trailing_step, account_id=account_id)
            elif trd_side == 'SELL':
                if close_id is None:
                    self.con.close_all_for_symbol(code, order_type=order_type, time_in_force=time_in_force,
                                                  account_id=account_id)
                else:
                    self.con.close_trade(close_id, qty, order_type=order_type, time_in_force=time_in_force, rate=rate,
                                         at_market=at_market)
            elif trd_side == 'COVER':
                if close_id is None:
                    self.con.close_all_for_symbol(code, order_type=order_type, time_in_force=time_in_force,
                                                  account_id=account_id)
                else:
                    self.con.close_trade(close_id, qty, order_type=order_type, time_in_force=time_in_force, rate=rate,
                                         at_market=at_market)
            else:
                return 0, 'Invalid trd_side: must be one of ["BUY", "SHORT", "SELL", "COVER"] but {} provided'.format(
                    trd_side)
        except ValueError as err:
            return 0, 'ValueError: {}'.format(err)
        except TypeError as err2:
            return 0, 'TypeError: {}'.format(err2)
        except Exception as e3:
            return 0, 'Exception: {}'.format(e3)

        return 1, ''

    def close_all(self, order_type='AtMarket', time_in_force='GTC',
                  account_id=None):
        try:
            self.con.close_all(order_type=order_type, time_in_force=time_in_force, account_id=account_id)
        except ValueError as err:
            return 0, 'ValueError: {}'.format(err)
        except TypeError as err2:
            return 0, 'TypeError: {}'.format(err2)
        except Exception as e3:
            return 0, 'Exception: {}'.format(e3)
        return 1, ''

    def modify_order(self, modify_order_op, order_id, qty, price, *args, **kwargs):
        pass

    def cancel_all_order(self, *args):
        pass

    def change_order(self, order_id, price, qty, *args, **kwargs):
        pass

    def acctradinginfo_query(self, *args, **kwargs):
        pass

    def deal_list_query(self, *args, **kwargs):
        pass

    def history_order_list_query(self, *args, **kwargs):
        pass

    def history_deal_list_query(self, *args, **kwargs):
        pass