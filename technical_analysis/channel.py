import pandas as pd
import numpy as np
from arctic import Arctic

from technical_analysis.overlap import BBANDS
from technical_analysis.utils import MA_Type

__overlap__ = True
__func__ = ['Bollinger_bands', 'Donchian_channels', 'Bollinger_Donchian']


def Bollinger_bands(inputs, period: int = 5, nbdevup: float = 2.0, nbdevdn: float = 2.0, matype: MA_Type = MA_Type.SMA,
                    price_type: str = 'close'):
    """

    :param inputs:
    :param period:
    :param nbdevup:
    :param nbdevdn:
    :param matype:
    :param price_type:
    :return:
    """
    return BBANDS(inputs, period=period, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype, price_type=price_type)


def Donchian_channels(inputs: pd.DataFrame, period: int = 14):
    """

    :param inputs:
    :param period:
    :return:
    """
    uc = inputs['high'].rolling(window=period).max()
    lc = inputs['low'].rolling(window=period).min()
    mc = (uc + lc) / 2
    df = pd.DataFrame()
    df['upperband'] = uc
    df['lowerband'] = lc
    df['middleband'] = mc
    return df


def Bollinger_Donchian(inputs, bb_period: int = 14,
                       nbdevup: float = 2.0,
                       nbdevdn: float = 2.0,
                       matype: MA_Type = MA_Type.SMA,
                       dc_period: int = 14
                       ):
    """

    :param inputs:
    :param bb_period:
    :param nbdevup:
    :param nbdevdn:
    :param matype:
    :param dc_period:
    :return:
    """
    df = pd.DataFrame(index=inputs.index)
    bb = Bollinger_bands(inputs, bb_period, nbdevup, nbdevdn, matype)
    donchian = Donchian_channels(inputs, dc_period)
    # bb['upperband'], 'middleband', 'lowerband'
    df['upperband'] = np.minimum(bb['upperband'], donchian['upperband'])
    df['lowerband'] = np.maximum(bb['lowerband'], donchian['lowerband'])
    df['middleband'] = (bb['middleband'] + donchian['middleband']) / 2
    return df


if __name__ == '__main__':
    store = Arctic('localhost')
    df = store['3000count'].read('EUR/USD').data
    # dc = Donchian_channels(df)
    bb_dc = Bollinger_Donchian(df)