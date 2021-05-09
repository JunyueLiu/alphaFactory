import pandas as pd

from technical_analysis.overlap import MA, EMA


def cross_up_event(fast: pd.Series, slow: pd.Series) -> pd.Series:
    t_0 = fast < slow # type: pd.Series
    t_1 = fast >= slow # type: pd.Series
    cross = t_0.shift(1) * t_1
    return pd.Series(1, cross[cross == 1].index)


def cross_down_event(fast: pd.Series, slow: pd.Series) -> pd.Series:
    t_0 = fast > slow # type: pd.Series
    t_1 = fast <= slow # type: pd.Series
    cross = t_0.shift(1) * t_1
    return pd.Series(-1, cross[cross == 1].index)

def sma_cross_up_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = MA(ohlc, period=fast_period)
    slow = MA(ohlc, period=slow_period)
    return cross_up_event(fast, slow)


def sma_cross_down_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = MA(ohlc, period=fast_period)
    slow = MA(ohlc, period=slow_period)
    return cross_down_event(fast, slow)

def ema_cross_up_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = EMA(ohlc, period=fast_period)
    slow = EMA(ohlc, period=slow_period)
    return cross_up_event(fast, slow)


def ema_cross_down_event(ohlc: pd.DataFrame, fast_period: int, slow_period: int) -> pd.Series:
    fast = EMA(ohlc, period=fast_period)
    slow = EMA(ohlc, period=slow_period)
    return cross_down_event(fast, slow)