import pandas as pd

from technical_analysis.customization import DUALTHRUST
from technical_analysis.overlap import MA, EMA


def cross_up_event(fast: pd.Series, slow: pd.Series, name:str) -> pd.Series:
    t_0 = fast < slow  # type: pd.Series
    t_1 = fast >= slow  # type: pd.Series
    cross = t_0.shift(1) * t_1
    return pd.Series(1, cross[cross == 1].index, name=name)


def cross_down_event(fast: pd.Series, slow: pd.Series, name) -> pd.Series:
    t_0 = fast > slow  # type: pd.Series
    t_1 = fast <= slow  # type: pd.Series
    cross = t_0.shift(1) * t_1
    return pd.Series(-1, cross[cross == 1].index, name=name)


def sma_cross_up_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = MA(ohlc, period=fast_period)
    slow = MA(ohlc, period=slow_period)
    return cross_up_event(fast, slow, 'sma_cross_up_{}_{}'.format(fast_period, slow_period))


def sma_cross_down_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = MA(ohlc, period=fast_period)
    slow = MA(ohlc, period=slow_period)
    return cross_down_event(fast, slow, 'sma_cross_down_{}_{}'.format(fast_period, slow_period))


def ema_cross_up_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = EMA(ohlc, period=fast_period)
    slow = EMA(ohlc, period=slow_period)
    return cross_up_event(fast, slow, name='ema_cross_up_{}_{}'.format(fast_period, slow_period))


def ema_cross_down_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = EMA(ohlc, period=fast_period)
    slow = EMA(ohlc, period=slow_period)
    return cross_down_event(fast, slow, name='ema_cross_down_{}_{}'.format(fast_period, slow_period))


def dualthrust_up_event(ohlc: pd.DataFrame, period: int = 14, k1: float = 0.2, k2: float = 0.2) -> pd.Series:
    fast = DUALTHRUST(ohlc, period=period, k1=k1, k2=k2)['buy_line']
    slow = ohlc['close']
    return cross_up_event(fast, slow, 'dualThrust_up_{}_{}_{}'.format(period, k1, k2))

def dualthrust_down_event(ohlc: pd.DataFrame, period: int = 14, k1: float = 0.2, k2: float = 0.2) -> pd.Series:
    fast = DUALTHRUST(ohlc, period=period, k1=k1, k2=k2)['sell_line']
    slow = ohlc['close']
    return cross_up_event(fast, slow, 'dualThrust_up_{}_{}_{}'.format(period, k1, k2))
