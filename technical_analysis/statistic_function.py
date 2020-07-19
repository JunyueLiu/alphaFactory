"""
"""
from talib import abstract
import numpy as np

from technical_analysis import utils

__overlap__ = False
__func__ = ['BETA',
            'CORREL',
            'LINEARREG',
            'LINEARREG_ANGLE',
            'LINEARREG_INTERCEPT',
            'LINEARREG_SLOPE',
            'STDDEV',
            'TSF',
            'VAR']


def BETA(inputs, timeperiod: int = 5, price0='high', price1='low'):
    """
    {'name': 'BETA',
    'group': 'Statistic Functions',
    'display_name': 'Beta',
    'function_flags': None,
     'input_names': OrderedDict([('price0', 'high'), ('price1', 'low')]),
     'parameters': OrderedDict([('timeperiod', 5)]), 'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :return:
    """
    indicator = abstract.Function('BETA')
    if not utils.check(inputs, [price0, price1]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price0=price0, price1=price1)


def CORREL(inputs, timeperiod: int = 30, price0='high', price1='low'):
    """
    {'name': 'CORREL',
    'group': 'Statistic Functions',
    'display_name': "Pearson's Correlation Coefficient (r)",
    'function_flags': None,
    'input_names': OrderedDict([('price0', 'high'), ('price1', 'low')]),
    'parameters': OrderedDict([('timeperiod', 30)]),
    'output_flags': OrderedDict([('real', ['Line'])]),
    'output_names': ['real']}

    :return:
    """
    indicator = abstract.Function('BETA')
    if not utils.check(inputs, [price0, price1]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price0=price0, price1=price1)


def LINEARREG(inputs, timeperiod: int = 14, price_type='close', ):
    """
    {'name': 'LINEARREG',
    'group': 'Statistic Functions',
    'display_name': 'Linear Regression',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('LINEARREG')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price=price_type)


def LINEARREG_ANGLE(inputs, timeperiod: int = 14, price_type='close'):
    """
    {'name': 'LINEARREG_ANGLE',
     'group': 'Statistic Functions',
     'display_name': 'Linear Regression Angle',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('LINEARREG_ANGLE')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price=price_type)


def LINEARREG_INTERCEPT(inputs, timeperiod: int = 14, price_type='close'):
    """
    {'name': 'LINEARREG_INTERCEPT',
     'group': 'Statistic Functions',
     'display_name': 'Linear Regression Intercept',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('LINEARREG_INTERCEPT')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price=price_type)


def LINEARREG_SLOPE(inputs, timeperiod: int = 14, price_type='close'):
    """
    {'name': 'LINEARREG_SLOPE',
     'group': 'Statistic Functions',
     'display_name': 'Linear Regression Slope',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('LINEARREG_SLOPE')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price=price_type)


def STDDEV(inputs, timeperiod: int = 14, nbdev: float = 1.0, price_type='close'):
    """
    {'name': 'STDDEV',
     'group': 'Statistic Functions',
     'display_name': 'Standard Deviation',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 5), ('nbdev', 1)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('STDDEV')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, nbdev=nbdev, price=price_type)


def TSF(inputs, timeperiod: int = 14, price_type='close'):
    """
    {'name': 'TSF',
     'group': 'Statistic Functions',
     'display_name': 'Time Series Forecast',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('TSF')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, price=price_type)


def VAR(inputs, timeperiod: int = 5, nbdev: float = 1.0, price_type='close'):
    """
    {'name': 'VAR',
     'group': 'Statistic Functions',
     'display_name': 'Variance',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 5), ('nbdev', 1)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :return:
    """
    indicator = abstract.Function('VAR')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=timeperiod, nbdev=nbdev, price=price_type)


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
