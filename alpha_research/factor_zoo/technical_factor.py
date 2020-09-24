import pandas as pd
from technical_analysis.momentum import *
from technical_analysis.overlap import *
from technical_analysis.volatility import *
from technical_analysis.volume import *

"""
overlap
"""


def ma(df, period: int = 30, matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: MA(x, period, matype, price_type)).droplevel(0).sort_index()
    else:
        return MA(df, period, matype, price_type)


def ema(df, period: int = 30, price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: EMA(x, period, price_type)).droplevel(0).sort_index()
    else:
        return EMA(df, period, price_type)


def ht_trendline(df, price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: HT_TRENDLINE(x, price_type)).droplevel(0).sort_index()
    else:
        return HT_TRENDLINE(df, price_type)

def sar(df, acceleration: float = 0.02, period: int = 14, prices=None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: SAR(x, acceleration, period, prices)).droplevel(0).sort_index()
    else:
        return SAR(df, acceleration, period, prices)



"""
momentum

"""


def adx(df: pd.DataFrame, period=14, prices: list or None = None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(lambda x: ADX(x, period=period, prices=prices)).droplevel(0).sort_index()
    else:
        return ADX(df, period=period, prices=prices)


def adxr(df: pd.DataFrame, period=14, prices: list or None = None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(lambda x: ADXR(x, period=period, prices=prices)).droplevel(0).sort_index()
    else:
        return ADXR(df, period=period, prices=prices)


def apo(df: pd.DataFrame, fastperiod: int = 12, slowperiod: int = 26, matype: MA_Type = MA_Type.SMA,
        price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(lambda x: APO(x, fastperiod, slowperiod, matype, price_type)).droplevel(
            0).sort_index()
    else:
        return APO(df, fastperiod, slowperiod, matype, price_type)


def macd(df: pd.DataFrame, fastperiod: int = 12, slowperiod: int = 26, signalperiod: int = 9,
         price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: MACD(x, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod,
                           price_type=price_type))
    else:
        return MACD(df, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod, price_type=price_type)


def mfi(df, period: int = 14, prices: list or None = None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: MFI(x, period=period, prices=prices)).droplevel(0).sort_index()
    else:
        return MFI(df, period=period, prices=prices)


def mom(df, period: int = 14, price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: MOM(x, period=period, price_type=price_type)).droplevel(0).sort_index()
    else:
        return MOM(df, period=period, price_type=price_type)


def ppo(df, fastperiod: int = 12, slowperiod: int = 26, matype: MA_Type = MA_Type.SMA, price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: PPO(x, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype,
                          price_type=price_type)).droplevel(0).sort_index()
    else:
        return PPO(df, fastperiod=fastperiod, slowperiod=slowperiod, matype=matype, price_type=price_type)


def rsi(df, period: int = 14, price_type: str = 'close'):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: RSI(x, period=period, price_type=price_type)).droplevel(0).sort_index()
    else:
        return RSI(df, period=period, price_type=price_type)


def willr(df, period: int = 14, prices: list or None = None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: WILLR(x, period=period, prices=prices)).droplevel(0).sort_index()
    else:
        return WILLR(df, period=period, prices=prices)


"""
volatility
"""


def atr(df, period: int = 14, prices=None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: ATR(x, period, prices)).droplevel(0).sort_index()
    else:
        return ATR(df, period, prices)


def natr(df, period: int = 14, prices=None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: NATR(x, period, prices)).droplevel(0).sort_index()
    else:
        return NATR(df, period, prices)


"""
volume
"""


def ad(df, prices=None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: AD(x, prices)).droplevel(0).sort_index()
    else:
        return AD(df, prices)


def adosc(df, fastperiod: int = 3, slowperiod: int = 10, prices=None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: ADOSC(x, fastperiod, slowperiod, prices)).droplevel(0).sort_index()
    else:
        return ADOSC(df, fastperiod, slowperiod, prices)


def obv(df, prices=None):
    if isinstance(df.index, pd.MultiIndex):
        return df.groupby(level=1).apply(
            lambda x: OBV(x, prices)).droplevel(0).sort_index()
    else:
        return OBV(df, prices)
