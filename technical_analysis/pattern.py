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

def CDL2CROWS(inputs):
    pass
