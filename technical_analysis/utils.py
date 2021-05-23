import pandas as pd
import numpy as np
from talib import abstract
from enum import Enum


class MA_Type(Enum):
    """
    MA_Type = {0: 'Simple Moving Average',
           1: 'Exponential Moving Average',
           2: 'Weighted Moving Average',
           3: 'Double Exponential Moving Average',
           4: 'Triple Exponential Moving Average',
           5: 'Triangular Moving Average',
           6: 'Kaufman Adaptive Moving Average',
           7: 'MESA Adaptive Moving Average',
           8: 'Triple Generalized Double Exponential Moving Average'}
    """
    SMA = 0
    EMA = 1
    WMA = 2
    DOUBLE_EMA = 3
    TRIPLE_EMA = 4
    TRIANGULAR_MA = 5
    KAUFMAN_ADAPTIVE_MA = 6
    MESA_ADAPTIVE_MA = 7
    TRIPLE_GENERALIZED_DOUBLE_EMA = 8


def check(inputs, input_names: list) -> bool:
    keys = []
    if isinstance(inputs, pd.DataFrame):
        keys = inputs.columns
    elif isinstance(inputs, dict):
        keys = inputs.keys()
    elif len(input_names) == 1 and isinstance(inputs, pd.Series):
        return True
    elif len(input_names) == 1 and isinstance(inputs, np.ndarray):
        return True

    return set(input_names).issubset(keys)
