"""
overlap studies
"""
from talib import abstract
import numpy as np

from technical_analysis import utils
from technical_analysis.utils import MA_Type

__overlap__ = True
__func__ = ['BBANDS',
            'DEMA',
            'EMA',
            'HT_TRENDLINE',
            'KAMA',
            'MA',
            'MAMA',
            'MAVP',
            'MIDPOINT',
            'MIDPRICE',
            'SAR',
            'SAREXT',
            'SMA',
            'T3',
            'TEMA',
            'TRIMA',
            'WMA']


def BBANDS(inputs, period: int = 5, nbdevup: float = 2.0, nbdevdn: float = 2.0, matype: MA_Type = MA_Type.SMA,
           price_type: str = 'close'):
    """
    {'name': 'BBANDS',
     'group': 'Overlap Studies',
     'display_name': 'Bollinger Bands',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 5),
                  ('nbdevup', 2),
                  ('nbdevdn', 2),
                  ('matype', 0)]),
     'output_flags': OrderedDict([('upperband',
                   ['Values represent an upper limit']),
                  ('middleband', ['Line']),
                  ('lowerband', ['Values represent a lower limit'])]),
     'output_names': ['upperband', 'middleband', 'lowerband']}
    :param inputs:
    :param period:
    :param nbdevup:
    :param nbdevdn:
    :param matype:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('BBANDS')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period,
                     nbdevup=nbdevup, nbdevdn=nbdevdn,
                     matype=matype.value, price=price_type
                     )


def DEMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'DEMA',
     'group': 'Overlap Studies',
     'display_name': 'Double Exponential Moving Average',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('DEMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def EMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'EMA',
     'group': 'Overlap Studies',
     'display_name': 'Exponential Moving Average',
     'function_flags': ['Output scale same as input',
      'Function has an unstable period'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('EMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def HT_TRENDLINE(inputs, price_type: str = 'close'):
    """
    {'name': 'HT_TRENDLINE',
     'group': 'Overlap Studies',
     'display_name': 'Hilbert Transform - Instantaneous Trendline',
     'function_flags': ['Output scale same as input',
      'Function has an unstable period'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('HT_TRENDLINE')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, price=price_type)


def KAMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'KAMA',
     'group': 'Overlap Studies',
     'display_name': 'Kaufman Adaptive Moving Average',
     'function_flags': ['Output scale same as input',
      'Function has an unstable period'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('KAMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def MA(inputs, period: int = 30, matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    """
    {'name': 'MA',
     'group': 'Overlap Studies',
     'display_name': 'Moving average',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30), ('matype', 0)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param matype:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('MA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, matype=matype.value, price=price_type)


def MAMA(inputs, fastlimit: int = 0.5, slowlimit: int = 0.05, price_type: str = 'close'):
    """
    {'name': 'MAMA',
    'group': 'Overlap Studies',
    'display_name': 'MESA Adaptive Moving Average',
    'function_flags': ['Output scale same as input',
    'Function has an unstable period'],
    'input_names': OrderedDict([('price', 'close')]),
    'parameters': OrderedDict([('fastlimit', 0.5), ('slowlimit', 0.05)]),
    'output_flags': OrderedDict([('mama', ['Line']), ('fama', ['Dashed Line'])]),
    'output_names': ['mama', 'fama']}
    :param inputs:
    :param fastlimit:
    :param slowlimit:
    :param price_type:
    :return:
    """

    indicator = abstract.Function('MAMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, fastlimit=fastlimit, slowlimit=slowlimit, price=price_type)


def MAVP(inputs, periods: str = 'periods', minperiod=2, maxperiod=30,
         matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    """
    {'name': 'MAVP',
     'group': 'Overlap Studies',
     'display_name': 'Moving average with variable period',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close'), ('periods', 'periods')]),
     'parameters': OrderedDict([('minperiod', 2),
                  ('maxperiod', 30),
                  ('matype', 0)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param minperiod:
    :param maxperiod:
    :param matype:
    :param price_type:
    :return:
    """

    indicator = abstract.Function('MAVP')
    if not utils.check(inputs, [price_type, periods]):
        raise ValueError('')
    return indicator(inputs, periods=periods, minperiod=minperiod, maxperiod=maxperiod,
                     matype=matype.value, price=price_type)


def MIDPOINT(inputs, period: int = 14, price_type: str = 'close'):
    """
    {'name': 'MIDPOINT',
     'group': 'Overlap Studies',
     'display_name': 'MidPoint over period',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('MIDPOINT')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def MIDPRICE(inputs, period: int = 14, prices=None):
    """
    {'name': 'MIDPRICE',
     'group': 'Overlap Studies',
     'display_name': 'Midpoint Price over period',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('prices', ['high', 'low'])]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param prices:
    :return:
    """

    if prices is None:
        prices = ['high', 'low']
    indicator = abstract.Function('MIDPRICE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def SAR(inputs, acceleration: float = 0.02, period: int = 14, prices=None):
    """
    {'name': 'SAR',
     'group': 'Overlap Studies',
     'display_name': 'Parabolic SAR',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('prices', ['high', 'low'])]),
     'parameters': OrderedDict([('acceleration', 0.02), ('maximum', 0.2)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param acceleration:
    :param period:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low']
    indicator = abstract.Function('SAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, acceleration=acceleration, timeperiod=period, prices=prices)


def SAREXT(inputs, offsetonreverse: float = 0.0,
           accelerationinitlong=0.02,
           accelerationlong=0.02,
           accelerationmaxlong=0.2,
           accelerationinitshort=0.02,
           accelerationshort=0.02,
           accelerationmaxshort=0.2, prices=None):
    """
    {'name': 'SAREXT',
     'group': 'Overlap Studies',
     'display_name': 'Parabolic SAR - Extended',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('prices', ['high', 'low'])]),
     'parameters': OrderedDict([('startvalue', 0),
                  ('offsetonreverse', 0),
                  ('accelerationinitlong', 0.02),
                  ('accelerationlong', 0.02),
                  ('accelerationmaxlong', 0.2),
                  ('accelerationinitshort', 0.02),
                  ('accelerationshort', 0.02),
                  ('accelerationmaxshort', 0.2)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
    'output_names': ['real']}
    :param inputs:
    :param offsetonreverse:
    :param accelerationinitlong:
    :param accelerationlong:
    :param accelerationmaxlong:
    :param accelerationinitshort:
    :param accelerationshort:
    :param accelerationmaxshort:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low']
    indicator = abstract.Function('SAREXT')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, offsetonreverse=offsetonreverse,
                     accelerationinitlong=accelerationinitlong,
                     accelerationlong=accelerationlong,
                     accelerationmaxlong=accelerationmaxlong,
                     accelerationinitshort=accelerationinitshort,
                     accelerationshort=accelerationshort,
                     accelerationmaxshort=accelerationmaxshort, prices=prices)


def SMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'SMA',
     'group': 'Overlap Studies',
     'display_name': 'Simple Moving Average',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('SMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def T3(inputs, period: int = 5, vfactor: int = 0.7, price_type: str = 'close'):
    """
    {'name': 'T3',
     'group': 'Overlap Studies',
     'display_name': 'Triple Exponential Moving Average (T3)',
     'function_flags': ['Output scale same as input',
      'Function has an unstable period'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 5), ('vfactor', 0.7)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param vfactor:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('T3')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, vfactor=vfactor, price=price_type)


def TEMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'TEMA',
     'group': 'Overlap Studies',
     'display_name': 'Triple Exponential Moving Average',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('SMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def TRIMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'TRIMA',
     'group': 'Overlap Studies',
     'display_name': 'Triangular Moving Average',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('TRIMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def WMA(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'WMA',
     'group': 'Overlap Studies',
     'display_name': 'Weighted Moving Average',
     'function_flags': ['Output scale same as input'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('WMA')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


if __name__ == '__main__':
    inputs = {
        'open': np.random.random(100),
        'high': np.random.random(100),
        'low': np.random.random(100),
        'close': np.random.random(100),
        'volume': np.random.random(100),
        'periods': np.random.random(100)
    }
    for f in __func__:
        try:
            ind = eval(f)(inputs)
        except:
            print(f)

    eval("MA(inputs,period=10,matype=0,price_type='close')")