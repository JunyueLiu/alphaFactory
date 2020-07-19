"""
pattern recognition
"""
from talib import abstract
import numpy as np

from technical_analysis import utils
from technical_analysis.utils import MA_Type

__overlap__ = False
__func__ = ['CDL2CROWS',
            'CDL3BLACKCROWS',
            'CDL3INSIDE',
            'CDL3LINESTRIKE',
            'CDL3OUTSIDE',
            'CDL3STARSINSOUTH',
            'CDL3WHITESOLDIERS',
            'CDLABANDONEDBABY',
            'CDLADVANCEBLOCK',
            'CDLBELTHOLD',
            'CDLBREAKAWAY',
            'CDLCLOSINGMARUBOZU',
            'CDLCONCEALBABYSWALL',
            'CDLCOUNTERATTACK',
            'CDLDARKCLOUDCOVER',
            'CDLDOJI',
            'CDLDOJISTAR',
            'CDLDRAGONFLYDOJI',
            'CDLENGULFING',
            'CDLEVENINGDOJISTAR',
            'CDLEVENINGSTAR',
            'CDLGAPSIDESIDEWHITE',
            'CDLGRAVESTONEDOJI',
            'CDLHAMMER',
            'CDLHANGINGMAN',
            'CDLHARAMI',
            'CDLHARAMICROSS',
            'CDLHIGHWAVE',
            'CDLHIKKAKE',
            'CDLHIKKAKEMOD',
            'CDLHOMINGPIGEON',
            'CDLIDENTICAL3CROWS',
            'CDLINNECK',
            'CDLINVERTEDHAMMER',
            'CDLKICKING',
            'CDLKICKINGBYLENGTH',
            'CDLLADDERBOTTOM',
            'CDLLONGLEGGEDDOJI',
            'CDLLONGLINE',
            'CDLMARUBOZU',
            'CDLMATCHINGLOW',
            'CDLMATHOLD',
            'CDLMORNINGDOJISTAR',
            'CDLMORNINGSTAR',
            'CDLONNECK',
            'CDLPIERCING',
            'CDLRICKSHAWMAN',
            'CDLRISEFALL3METHODS',
            'CDLSEPARATINGLINES',
            'CDLSHOOTINGSTAR',
            'CDLSHORTLINE',
            'CDLSPINNINGTOP',
            'CDLSTALLEDPATTERN',
            'CDLSTICKSANDWICH',
            'CDLTAKURI',
            'CDLTASUKIGAP',
            'CDLTHRUSTING',
            'CDLTRISTAR',
            'CDLUNIQUE3RIVER',
            'CDLUPSIDEGAP2CROWS',
            'CDLXSIDEGAP3METHODS']


def CDL2CROWS(inputs, prices: list or None = None):
    """
    {'name': 'CDL2CROWS', 'group': 'Pattern Recognition', 'display_name': 'Two Crows',
              'function_flags': ['Output is a candlestick'],
              'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
              'parameters': OrderedDict(),
              'output_flags': OrderedDict([('integer', ['Line'])]), 'output_names': ['integer']}
    :param inputs:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL2CROWS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDL3BLACKCROWS(inputs, prices: list or None = None):
    """
    {'name': 'CDL3BLACKCROWS',
     'group': 'Pattern Recognition',
     'display_name': 'Three Black Crows',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL3BLACKCROWS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDL3INSIDE(inputs, prices: list or None = None):
    """
    {'name': 'CDL3INSIDE',
     'group': 'Pattern Recognition',
     'display_name': 'Three Inside Up/Down',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL3INSIDE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDL3LINESTRIKE(inputs, prices: list or None = None):
    """
    {'name': 'CDL3LINESTRIKE',
     'group': 'Pattern Recognition',
     'display_name': 'Three-Line Strike ',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL3LINESTRIKE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDL3OUTSIDE(inputs, prices: list or None = None):
    """
    {'name': 'CDL3OUTSIDE',
     'group': 'Pattern Recognition',
     'display_name': 'Three Outside Up/Down',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL3OUTSIDE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDL3STARSINSOUTH(inputs, prices: list or None = None):
    """
    {'name': 'CDL3STARSINSOUTH',
     'group': 'Pattern Recognition',
     'display_name': 'Three Stars In The South',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL3STARSINSOUTH')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDL3WHITESOLDIERS(inputs, prices: list or None = None):
    """
    {'name': 'CDL3WHITESOLDIERS',
     'group': 'Pattern Recognition',
     'display_name': 'Three Advancing White Soldiers',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDL3WHITESOLDIERS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLABANDONEDBABY(inputs, penetration: float = 0.3, prices: list or None = None):
    """
    {'name': 'CDLABANDONEDBABY',
     'group': 'Pattern Recognition',
     'display_name': 'Abandoned Baby',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.3)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLABANDONEDBABY')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, penetration=penetration)


def CDLADVANCEBLOCK(inputs, prices: list or None = None):
    """
    {'name': 'CDLADVANCEBLOCK',
     'group': 'Pattern Recognition',
     'display_name': 'Advance Block',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLADVANCEBLOCK')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLBELTHOLD(inputs, prices: list or None = None):
    """
    {'name': 'CDLBELTHOLD',
     'group': 'Pattern Recognition',
     'display_name': 'Belt-hold',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLBELTHOLD')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLBREAKAWAY(inputs, prices: list or None = None):
    """
    {'name': 'CDLBREAKAWAY',
     'group': 'Pattern Recognition',
     'display_name': 'Breakaway',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLBREAKAWAY')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLCLOSINGMARUBOZU(inputs, prices: list or None = None):
    """
    {'name': 'CDLCLOSINGMARUBOZU',
     'group': 'Pattern Recognition',
     'display_name': 'Closing Marubozu',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLCLOSINGMARUBOZU')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLCONCEALBABYSWALL(inputs, prices: list or None = None):
    """
    {'name': 'CDLCONCEALBABYSWALL',
     'group': 'Pattern Recognition',
     'display_name': 'Concealing Baby Swallow',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLCONCEALBABYSWALL')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLCOUNTERATTACK(inputs, prices: list or None = None):
    """
    {'name': 'CDLCOUNTERATTACK',
     'group': 'Pattern Recognition',
     'display_name': 'Counterattack',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLCOUNTERATTACK')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLDARKCLOUDCOVER(inputs, penetration: float = 0.5, prices: list or None = None):
    """
    {'name': 'CDLDARKCLOUDCOVER',
     'group': 'Pattern Recognition',
     'display_name': 'Dark Cloud Cover',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.5)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param penetration:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLDARKCLOUDCOVER')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, penetration=penetration)


def CDLDOJI(inputs, prices: list or None = None):
    """
    {'name': 'CDLDOJI',
     'group': 'Pattern Recognition',
     'display_name': 'Doji',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLDOJI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLDOJISTAR(inputs, prices: list or None = None):
    """
    {'name': 'CDLDOJISTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Doji Star',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLDOJISTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLDRAGONFLYDOJI(inputs, prices: list or None = None):
    """
    {'name': 'CDLDRAGONFLYDOJI',
     'group': 'Pattern Recognition',
     'display_name': 'Dragonfly Doji',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLDRAGONFLYDOJI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLENGULFING(inputs, prices: list or None = None):
    """
    {'name': 'CDLENGULFING',
     'group': 'Pattern Recognition',
     'display_name': 'Engulfing Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLENGULFING')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLEVENINGDOJISTAR(inputs, penetration: float = 0.3, prices: list or None = None):
    """
    {'name': 'CDLEVENINGDOJISTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Evening Doji Star',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.3)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}

    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLEVENINGDOJISTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, penetration=penetration)


def CDLEVENINGSTAR(inputs, penetration: float = 0.3, prices: list or None = None):
    """
    {'name': 'CDLEVENINGSTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Evening Star',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.3)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLEVENINGSTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, penetration=penetration)


def CDLGAPSIDESIDEWHITE(inputs, prices: list or None = None):
    """
    {'name': 'CDLGAPSIDESIDEWHITE',
     'group': 'Pattern Recognition',
     'display_name': 'Up/Down-gap side-by-side white lines',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}

    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLGAPSIDESIDEWHITE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLGRAVESTONEDOJI(inputs, prices: list or None = None):
    """
    {'name': 'CDLGRAVESTONEDOJI',
     'group': 'Pattern Recognition',
     'display_name': 'Gravestone Doji',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLGRAVESTONEDOJI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHAMMER(inputs, prices: list or None = None):
    """
    {'name': 'CDLHAMMER',
     'group': 'Pattern Recognition',
     'display_name': 'Hammer',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHAMMER')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHANGINGMAN(inputs, prices: list or None = None):
    """
    {'name': 'CDLHANGINGMAN',
     'group': 'Pattern Recognition',
     'display_name': 'Hanging Man',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHANGINGMAN')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHARAMI(inputs, prices: list or None = None):
    """
    {'name': 'CDLHARAMI',
     'group': 'Pattern Recognition',
     'display_name': 'Harami Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHARAMI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHARAMICROSS(inputs, prices: list or None = None):
    """
    {'name': 'CDLHARAMICROSS',
     'group': 'Pattern Recognition',
     'display_name': 'Harami Cross Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHARAMICROSS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHIGHWAVE(inputs, prices: list or None = None):
    """
    {'name': 'CDLHIGHWAVE',
     'group': 'Pattern Recognition',
     'display_name': 'High-Wave Candle',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHIGHWAVE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHIKKAKE(inputs, prices: list or None = None):
    """
    {'name': 'CDLHIKKAKE',
     'group': 'Pattern Recognition',
     'display_name': 'Hikkake Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHIKKAKE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHIKKAKEMOD(inputs, prices: list or None = None):
    """
    {'name': 'CDLHIKKAKEMOD',
     'group': 'Pattern Recognition',
     'display_name': 'Modified Hikkake Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHIKKAKEMOD')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLHOMINGPIGEON(inputs, prices: list or None = None):
    """
    {'name': 'CDLHOMINGPIGEON',
     'group': 'Pattern Recognition',
     'display_name': 'Homing Pigeon',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLHOMINGPIGEON')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLIDENTICAL3CROWS(inputs, prices: list or None = None):
    """
    {'name': 'CDLIDENTICAL3CROWS',
     'group': 'Pattern Recognition',
     'display_name': 'Identical Three Crows',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLIDENTICAL3CROWS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLINNECK(inputs, prices: list or None = None):
    """
    {'name': 'CDLINNECK',
     'group': 'Pattern Recognition',
     'display_name': 'In-Neck Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}

    :param inputs:
    :param prices:
    :return:
    """

    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLINNECK')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLINVERTEDHAMMER(inputs, prices: list or None = None):
    """
    {'name': 'CDLINVERTEDHAMMER',
     'group': 'Pattern Recognition',
     'display_name': 'Inverted Hammer',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLINVERTEDHAMMER')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLKICKING(inputs, prices: list or None = None):
    """
    {'name': 'CDLKICKING',
     'group': 'Pattern Recognition',
     'display_name': 'Kicking',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLKICKING')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLKICKINGBYLENGTH(inputs, prices: list or None = None):
    """

    {'name': 'CDLKICKINGBYLENGTH',
     'group': 'Pattern Recognition',
     'display_name': 'Kicking - bull/bear determined by the longer marubozu',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLKICKINGBYLENGTH')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLLADDERBOTTOM(inputs, prices: list or None = None):
    """
    {'name': 'CDLLADDERBOTTOM',
     'group': 'Pattern Recognition',
     'display_name': 'Ladder Bottom',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLLADDERBOTTOM')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLLONGLEGGEDDOJI(inputs, prices: list or None = None):
    """
    {'name': 'CDLLONGLEGGEDDOJI',
     'group': 'Pattern Recognition',
     'display_name': 'Long Legged Doji',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLLONGLEGGEDDOJI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLLONGLINE(inputs, prices: list or None = None):
    """
    {'name': 'CDLLONGLINE',
     'group': 'Pattern Recognition',
     'display_name': 'Long Line Candle',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLLONGLINE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLMARUBOZU(inputs, prices: list or None = None):
    """
    {'name': 'CDLMARUBOZU',
     'group': 'Pattern Recognition',
     'display_name': 'Marubozu',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}

    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLMARUBOZU')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLMATCHINGLOW(inputs, prices: list or None = None):
    """
    {'name': 'CDLMATCHINGLOW',
     'group': 'Pattern Recognition',
     'display_name': 'Matching Low',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLMATCHINGLOW')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLMATHOLD(inputs, penetration: float = 0.5, prices: list or None = None):
    """
    {'name': 'CDLMATHOLD',
     'group': 'Pattern Recognition',
     'display_name': 'Mat Hold',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.5)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLMATHOLD')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs, penetration=penetration)


def CDLMORNINGDOJISTAR(inputs, prices: list or None = None):
    """
    {'name': 'CDLMORNINGDOJISTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Morning Doji Star',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.3)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLMORNINGDOJISTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLMORNINGSTAR(inputs, prices: list or None = None):
    """
    {'name': 'CDLMORNINGSTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Morning Star',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict([('penetration', 0.3)]),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLMORNINGSTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLONNECK(inputs, prices: list or None = None):
    """
    {'name': 'CDLONNECK',
     'group': 'Pattern Recognition',
     'display_name': 'On-Neck Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLONNECK')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLPIERCING(inputs, prices: list or None = None):
    """
    {'name': 'CDLPIERCING',
     'group': 'Pattern Recognition',
     'display_name': 'Piercing Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLPIERCING')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLRICKSHAWMAN(inputs, prices: list or None = None):
    """
    {'name': 'CDLRICKSHAWMAN',
     'group': 'Pattern Recognition',
     'display_name': 'Rickshaw Man',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLRICKSHAWMAN')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLRISEFALL3METHODS(inputs, prices: list or None = None):
    """
    {'name': 'CDLRISEFALL3METHODS',
     'group': 'Pattern Recognition',
     'display_name': 'Rising/Falling Three Methods',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLRISEFALL3METHODS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLSEPARATINGLINES(inputs, prices: list or None = None):
    """
    {'name': 'CDLSEPARATINGLINES',
     'group': 'Pattern Recognition',
     'display_name': 'Separating Lines',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLSEPARATINGLINES')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLSHOOTINGSTAR(inputs, prices: list or None = None):
    """
    {'name': 'CDLSHOOTINGSTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Shooting Star',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLSHOOTINGSTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLSHORTLINE(inputs, prices: list or None = None):
    """
    {'name': 'CDLSHORTLINE',
     'group': 'Pattern Recognition',
     'display_name': 'Short Line Candle',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLSHORTLINE')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLSPINNINGTOP(inputs, prices: list or None = None):
    """
    {'name': 'CDLSPINNINGTOP',
     'group': 'Pattern Recognition',
     'display_name': 'Spinning Top',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLSPINNINGTOP')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLSTALLEDPATTERN(inputs, prices: list or None = None):
    """
    {'name': 'CDLSTALLEDPATTERN',
     'group': 'Pattern Recognition',
     'display_name': 'Stalled Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """

    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLSTALLEDPATTERN')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLSTICKSANDWICH(inputs, prices: list or None = None):
    """
    {'name': 'CDLSTICKSANDWICH',
     'group': 'Pattern Recognition',
     'display_name': 'Stick Sandwich',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLSTICKSANDWICH')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLTAKURI(inputs, prices: list or None = None):
    """
    {'name': 'CDLTAKURI',
     'group': 'Pattern Recognition',
     'display_name': 'Takuri (Dragonfly Doji with very long lower shadow)',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLTAKURI')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLTASUKIGAP(inputs, prices: list or None = None):
    """
    {'name': 'CDLTASUKIGAP',
     'group': 'Pattern Recognition',
     'display_name': 'Tasuki Gap',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLTASUKIGAP')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLTHRUSTING(inputs, prices: list or None = None):
    """
    {'name': 'CDLTHRUSTING',
     'group': 'Pattern Recognition',
     'display_name': 'Thrusting Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLTHRUSTING')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLTRISTAR(inputs, prices: list or None = None):
    """
    {'name': 'CDLTRISTAR',
     'group': 'Pattern Recognition',
     'display_name': 'Tristar Pattern',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLTRISTAR')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLUNIQUE3RIVER(inputs, prices: list or None = None):
    """
    {'name': 'CDLUNIQUE3RIVER',
     'group': 'Pattern Recognition',
     'display_name': 'Unique 3 River',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLUNIQUE3RIVER')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLUPSIDEGAP2CROWS(inputs, prices: list or None = None):
    """
    {'name': 'CDLUPSIDEGAP2CROWS',
     'group': 'Pattern Recognition',
     'display_name': 'Upside Gap Two Crows',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLUPSIDEGAP2CROWS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


def CDLXSIDEGAP3METHODS(inputs, prices: list or None = None):
    """
    {'name': 'CDLXSIDEGAP3METHODS',
     'group': 'Pattern Recognition',
     'display_name': 'Upside/Downside Gap Three Methods',
     'function_flags': ['Output is a candlestick'],
     'input_names': OrderedDict([('prices', ['open', 'high', 'low', 'close'])]),
     'parameters': OrderedDict(),
     'output_flags': OrderedDict([('integer', ['Line'])]),
     'output_names': ['integer']}
    :param inputs:
    :param prices:
    :return:
    """
    if prices is None:
        prices = ['open', 'high', 'low', 'close']

    indicator = abstract.Function('CDLXSIDEGAP3METHODS')
    if not utils.check(inputs, prices):
        raise ValueError('')
    return indicator(inputs)


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
