"""
Momentum Indicators
"""
from talib import abstract
import numpy as np

from technical_analysis import utils
from technical_analysis.utils import MA_Type
import pandas as pd

__overlap__ = False
__func__ = ['ADX',
            'ADXR',
            'APO',
            'AROON',
            'AROONOSC',
            'BOP',
            'CCI',
            'CMO',
            'DX',
            'MACD',
            'MACDEXT',
            'MACDFIX',
            'MFI',
            'MINUS_DI',
            'MINUS_DM',
            'MOM',
            'PLUS_DI',
            'PLUS_DM',
            'PPO',
            'ROC',
            'ROCP',
            'ROCR',
            'ROCR100',
            'RSI',
            'STOCH',
            'STOCHF',
            'STOCHRSI',
            'TRIX',
            'ULTOSC',
            'WILLR']


def ADX(inputs, period=14, prices: list or None = None):
    """

    https://www.investopedia.com/terms/a/adx.asp

    {'name': 'ADX',
    'group': 'Momentum Indicators',
    'display_name': 'Average Directional Movement Index',
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
    indicator = abstract.Function('ADX')
    if not utils.check(inputs, prices):
        raise ValueError('Expect {} in the inputs. But only {}'.format(str(prices),
                                                                       str(inputs.columns)
                                                                       if isinstance(inputs, pd.DataFrame)
                                                                       else inputs.keys()))
    return indicator(inputs, timeperiod=period, prices=prices)


def ADXR(inputs, period=14, prices: list or None = None):
    """
    {'name': 'ADXR',
    'group': 'Momentum Indicators',
    'display_name': 'Average Directional Movement Index Rating',
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

    indicator = abstract.Function('ADXR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def APO(inputs, fastperiod: int = 12, slowperiod: int = 26, matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    """
    {'name': 'APO',
     'group': 'Momentum Indicators',
     'display_name': 'Absolute Price Oscillator',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('fastperiod', 12),
                                ('slowperiod', 26),
                                ('matype', 0)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param fastperiod:
    :param slowperiod:
    :param matype:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('APO')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype.value, price=price_type)


def AROON(inputs, period=14, prices: list or None = None):
    """
    {'name': 'AROON',
    'group': 'Momentum Indicators',
    'display_name': 'Aroon',
    'function_flags': None,
    'input_names': OrderedDict([('prices', ['high', 'low'])]),
    'parameters': OrderedDict([('timeperiod', 14)]),
    'output_flags': OrderedDict([('aroondown', ['Dashed Line']),
              ('aroonup', ['Line'])]),
    'output_names': ['aroondown', 'aroonup']}


    :param inputs:
    :param period:
    :param prices:
    :return: ['aroondown', 'aroonup']
    """
    if prices is None:
        prices = ['high', 'low']

    indicator = abstract.Function('AROON')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def AROONOSC(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'AROONOSC',
     'group': 'Momentum Indicators',
     'display_name': 'Aroon Oscillator',
     'function_flags': None,
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
    indicator = abstract.Function('AROONOSC')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def BOP(inputs, prices: list or None = None):
    """
    {'name': 'BOP',
    'group': 'Momentum Indicators',
     'display_name': 'Balance Of Power',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param prices:
    :return:
    """

    if prices is None:
        prices = ['open', 'high', 'low', 'close']
    indicator = abstract.Function('BOP')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, prices=prices)


def CCI(inputs, period: int = 14, prices: list or None = None):
    """
    https://www.investopedia.com/articles/active-trading/031914/how-traders-can-utilize-cci-commodity-channel-index-trade-stock-trends.asp
    {'name': 'CCI',
     'group': 'Momentum Indicators',
     'display_name': 'Commodity Channel Index',
     'function_flags': None,
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
    indicator = abstract.Function('CCI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def CMO(inputs, period: int = 14, price_type: str = 'close'):
    """
    {'name': 'CMO',
    'group': 'Momentum Indicators',
    'display_name': 'Chande Momentum Oscillator',
    'function_flags': ['Function has an unstable period'],
    'input_names': OrderedDict([('price', 'close')]),
    'parameters': OrderedDict([('timeperiod', 14)]),
    'output_flags': OrderedDict([('real', ['Line'])]),
    'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('CMO')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def DX(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'DX',
     'group': 'Momentum Indicators',
     'display_name': 'Directional Movement Index',
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
    indicator = abstract.Function('DX')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def MACD(inputs, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9, price_type: str = 'close'):
    """
    {'name': 'MACD',
     'group': 'Momentum Indicators',
     'display_name': 'Moving Average Convergence/Divergence',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('fastperiod', 12),
                  ('slowperiod', 26),
                  ('signalperiod', 9)]),
     'output_flags': OrderedDict([('macd', ['Line']),
                  ('macdsignal', ['Dashed Line']),
                  ('macdhist', ['Histogram'])]),
     'output_names': ['macd', 'macdsignal', 'macdhist']}
    :param inputs:
    :param fastperiod:
    :param slowperiod:
    :param signalperiod:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('MACD')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod, price=price_type)


def MACDEXT(inputs, fastperiod: int = 12, fastmatype: MA_Type = MA_Type.SMA,
            slowperiod: int = 26, slowmatype: MA_Type = MA_Type.SMA,
            signalperiod: int = 9, signalmatype: MA_Type = MA_Type.SMA,
            price_type: str = 'close'
            ):
    """
    {'name': 'MACDEXT',
     'group': 'Momentum Indicators',
     'display_name': 'MACD with controllable MA type',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('fastperiod', 12),
                  ('fastmatype', 0),
                  ('slowperiod', 26),
                  ('slowmatype', 0),
                  ('signalperiod', 9),
                  ('signalmatype', 0)]),
     'output_flags': OrderedDict([('macd', ['Line']),
                  ('macdsignal', ['Dashed Line']),
                  ('macdhist', ['Histogram'])]),
     'output_names': ['macd', 'macdsignal', 'macdhist']}
    :param inputs:
    :param fastperiod:
    :param fastmatype:
    :param slowperiod:
    :param slowmatype:
    :param signalperiod:
    :param signalmatype:
    :param price_type:
    :return:
    """

    indicator = abstract.Function('MACDEXT')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, fastperiod=fastperiod, fastmatype=fastmatype.value,
                     slowperiod=slowperiod, slowmatype=slowmatype.value,
                     signalperiod=signalperiod, signalmatype=signalmatype.value,
                     price=price_type)


def MACDFIX(inputs, signalperiod: int = 9, price_type: str = 'close'):
    """
    {'name': 'MACDFIX',
     'group': 'Momentum Indicators',
     'display_name': 'Moving Average Convergence/Divergence Fix 12/26',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('signalperiod', 9)]),
     'output_flags': OrderedDict([('macd', ['Line']),
                  ('macdsignal', ['Dashed Line']),
                  ('macdhist', ['Histogram'])]),
     'output_names': ['macd', 'macdsignal', 'macdhist']}
    :param inputs:
    :param signalperiod:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('MACDFIX')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, signalperiod=signalperiod, price=price_type)


def MFI(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'MFI',
     'group': 'Momentum Indicators',
     'display_name': 'Money Flow Index',
     'function_flags': ['Function has an unstable period'],
     'input_names': OrderedDict([('prices', ['high', 'low', 'close', 'volume'])]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close', 'volume']
    indicator = abstract.Function('MFI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def MINUS_DI(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'MINUS_DI',
     'group': 'Momentum Indicators',
     'display_name': 'Minus Directional Indicator',
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
    indicator = abstract.Function('MINUS_DI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def MINUS_DM(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'MINUS_DM',
     'group': 'Momentum Indicators',
     'display_name': 'Minus Directional Movement',
     'function_flags': ['Function has an unstable period'],
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
    indicator = abstract.Function('MINUS_DM')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def MOM(inputs, period: int = 14, price_type: str = 'close'):
    """
    {'name': 'MOM',
     'group': 'Momentum Indicators',
     'display_name': 'Momentum',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 10)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('MOM')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def PLUS_DI(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'PLUS_DI',
     'group': 'Momentum Indicators',
     'display_name': 'Plus Directional Indicator',
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
    indicator = abstract.Function('PLUS_DI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def PLUS_DM(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'PLUS_DM',
     'group': 'Momentum Indicators',
     'display_name': 'Plus Directional Movement',
     'function_flags': ['Function has an unstable period'],
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
    indicator = abstract.Function('PLUS_DM')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


def PPO(inputs, fastperiod: int = 12, slowperiod: int = 26, matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    """
    {'name': 'PPO',
     'group': 'Momentum Indicators',
     'display_name': 'Percentage Price Oscillator',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('fastperiod', 12),
                  ('slowperiod', 26),
                  ('matype', 0)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param fastperiod:
    :param slowperiod:
    :param matype:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('PPO')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype.value, price=price_type)


def ROC(inputs, period: int = 10, price_type: str = 'close'):
    """
    {'name': 'ROC',
     'group': 'Momentum Indicators',
     'display_name': 'Rate of change : ((price/prevPrice)-1)*100',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 10)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('ROC')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def ROCP(inputs, period: int = 10, price_type: str = 'close'):
    """
    {'name': 'ROCP',
     'group': 'Momentum Indicators',
     'display_name': 'Rate of change Percentage: (price-prevPrice)/prevPrice',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 10)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('ROCP')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def ROCR(inputs, period: int = 10, price_type: str = 'close'):
    """
    {'name': 'ROCR',
     'group': 'Momentum Indicators',
     'display_name': 'Rate of change ratio: (price/prevPrice)',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 10)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """

    indicator = abstract.Function('ROCR')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def ROCR100(inputs, period: int = 10, price_type: str = 'close'):
    """
    {'name': 'ROCR100',
     'group': 'Momentum Indicators',
     'display_name': 'Rate of change ratio 100 scale: (price/prevPrice)*100',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 10)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('ROCR100')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def RSI(inputs, period: int = 14, price_type: str = 'close'):
    """
    {'name': 'RSI',
     'group': 'Momentum Indicators',
     'display_name': 'Relative Strength Index',
     'function_flags': ['Function has an unstable period'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('RSI')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def STOCH(inputs, fastk_period: int = 5,
          slowk_period: int = 3,
          slowk_matype: MA_Type = MA_Type.SMA,
          slowd_period: int = 3,
          slowd_matype: MA_Type = MA_Type.SMA, prices: list or None = None):
    """
    {'name': 'STOCH',
     'group': 'Momentum Indicators',
     'display_name': 'Stochastic',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict([('fastk_period', 5),
                  ('slowk_period', 3),
                  ('slowk_matype', 0),
                  ('slowd_period', 3),
                  ('slowd_matype', 0)]),
     'output_flags': OrderedDict([('slowk', ['Dashed Line']),
                  ('slowd', ['Dashed Line'])]),
     'output_names': ['slowk', 'slowd']}
    :param inputs:
    :param fastk_period:
    :param slowk_period:
    :param slowk_matype:
    :param slowd_period:
    :param slowd_matype:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('STOCH')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, fastk_period=fastk_period,
                     slowk_period=slowk_period,
                     slowk_matype=slowk_matype.value,
                     slowd_period=slowd_period,
                     slowd_matype=slowd_matype.value,
                     prices=prices)


def STOCHF(inputs, fastk_period: int = 5,
           fastd_period: int = 3,
           fastd_matype: MA_Type = MA_Type.SMA, prices: list or None = None):
    """
    {'name': 'STOCHF',
     'group': 'Momentum Indicators',
     'display_name': 'Stochastic Fast',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict([('fastk_period', 5),
                  ('fastd_period', 3),
                  ('fastd_matype', 0)]),
     'output_flags': OrderedDict([('fastk', ['Line']), ('fastd', ['Line'])]),
     'output_names': ['fastk', 'fastd']}

    :param inputs:
    :param fastk_period:
    :param fastd_period:
    :param fastd_matype:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('STOCHF')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, fastk_period=fastk_period,
                     fastd_period=fastd_period,
                     fastd_matype=fastd_matype.value, prices=prices)


def STOCHRSI(inputs, period: int = 14, fastk_period: int = 5,
             fastd_period: int = 3,
             fastd_matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    """
    {'name': 'STOCHRSI',
     'group': 'Momentum Indicators',
     'display_name': 'Stochastic Relative Strength Index',
     'function_flags': ['Function has an unstable period'],
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 14),
                  ('fastk_period', 5),
                  ('fastd_period', 3),
                  ('fastd_matype', 0)]),
     'output_flags': OrderedDict([('fastk', ['Line']), ('fastd', ['Line'])]),
     'output_names': ['fastk', 'fastd']}
    :param inputs:
    :param period:
    :param fastk_period:
    :param fastd_period:
    :param fastd_matype:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('STOCHRSI')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, fastk_period=fastk_period,
                     fastd_period=fastd_period,
                     fastd_matype=fastd_matype.value,
                     price=price_type)


def TRIX(inputs, period: int = 30, price_type: str = 'close'):
    """
    {'name': 'TRIX',
     'group': 'Momentum Indicators',
     'display_name': '1-day Rate-Of-Change (ROC) of a Triple Smooth EMA',
     'function_flags': None,
     'input_names': OrderedDict([('price', 'close')]),
     'parameters': OrderedDict([('timeperiod', 30)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period:
    :param price_type:
    :return:
    """
    indicator = abstract.Function('TRIX')
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, price=price_type)


def ULTOSC(inputs, period1: int = 7, period2: int = 14, period3: int = 28, prices: list or None = None):
    """
    {'name': 'ULTOSC',
     'group': 'Momentum Indicators',
     'display_name': 'Ultimate Oscillator',
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict([('timeperiod1', 7),
                  ('timeperiod2', 14),
                  ('timeperiod3', 28)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}
    :param inputs:
    :param period1:
    :param period2:
    :param period3:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('ULTOSC')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod1=period1, timeperiod2=period2, timeperiod3=period3, prices=prices)


def WILLR(inputs, period: int = 14, prices: list or None = None):
    """
    {'name': 'WILLR',
     'group': 'Momentum Indicators',
     'display_name': "Williams' %R",
     'function_flags': None,
     'input_names': OrderedDict([('prices', ['high', 'low', 'close'])]),
     'parameters': OrderedDict([('timeperiod', 14)]),
     'output_flags': OrderedDict([('real', ['Line'])]),
     'output_names': ['real']}

    :param prices:
    :param inputs:
    :param period:
    :return:
    """
    if prices is None:
        prices = ['high', 'low', 'close']
    indicator = abstract.Function('WILLR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, timeperiod=period, prices=prices)


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

    data = pd.DataFrame(inputs)
