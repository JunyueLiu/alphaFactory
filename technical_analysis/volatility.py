"""
volatility Indicators
"""
from talib import abstract
import numpy as np

from technical_analysis import utils
from technical_analysis.utils import MA_Type

__overlap__ = False
__func__ = ['ATR', 'NATR', 'TRANGE']


def ATR(inputs, period: int = 14, prices=None):
    """
    {'name': 'ATR',
     'group': 'Volatility Indicators',
     'display_name': 'Average True Range',
     'function_flags': ['Function has an unstable period'],
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('ATR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def NATR(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'NATR',
     'group': 'Volatility Indicators',
     'display_name': 'Normalized Average True Range',
     'function_flags': ['Function has an unstable period'],
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('NATR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def TRANGE(inputs, prices: list or None = None):
    """
    {'name': 'TRANGE',
     'group': 'Volatility Indicators',
     'display_name': 'True Range',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('TRANGE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, prices=prices)

if __name__ == '__main__':
    inputs = {
        'open': np.random.random(100),
        'high': np.random.random(100),
        'low': np.random.random(100),
        'close': np.random.random(100),
        'volume': np.random.random(100)
    }
    for f in __func__:
        try:
            ind = eval(f)(inputs)
        except:
            print(f)