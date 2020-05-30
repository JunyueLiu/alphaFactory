"""
volume Indicators
"""
from talib import abstract
import numpy as np

from technical_analysis import utils
from technical_analysis.utils import MA_Type

__overlap__ = False
__func__ = ['AD', 'ADOSC', 'OBV']


def AD(inputs, prices=None):
    """
    {'name': 'AD',
     'group': 'Volume Indicators',
     'display_name': 'Chaikin A/D Line',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close', 'volume'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close', 'volume']
    indicator = abstract.Function('AD')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, prices=prices)


def ADOSC(inputs, fastperiod: int = 3, slowperiod: int = 10, prices=None):
    """
    {'name': 'ADOSC',
     'group': 'Volume Indicators',
     'display_name': 'Chaikin A/D Oscillator',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close', 'volume'])]),
     'parameters': OrderedDict([('fastperiod', 3), ('slowperiod', 10)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param fastperiod:
    :param slowperiod:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close', 'volume']
    indicator = abstract.Function('ADOSC')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, fastperiod=fastperiod, slowperiod=slowperiod, prices=prices)


def OBV(inputs, prices=None):
    """
    {'name': 'OBV',
     'group': 'Volume Indicators',
     'display_name': 'On Balance Volume',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close'), ('prices', ['volume'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['close', 'volume']
    indicator = abstract.Function('OBV')
    if not utils.check(inputs, prices):
        raise ValueError('')
    volume = inputs[prices[1]]
    return indicator(inputs, volume, price = prices[0], prices=[prices[1]])


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
