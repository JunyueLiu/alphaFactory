from scipy import sparse
from scipy.sparse.linalg import spsolve

from technical_analysis.momentum import MOM
from technical_analysis.overlap import EMA, MIDPRICE
from technical_analysis.volatility import TRANGE
from technical_analysis import utils
import numpy as np
import pandas as pd

__func__ = [
    'DUALTHRUST',
    'MAMOM_CLIP',
    'SECONDARY_MOM',
    'SUPERTREND'

]


def DUALTHRUST(inputs, period: int = 14, k1=0.1, k2=0.1):
    if isinstance(inputs, dict):
        inputs_ = pd.DataFrame(inputs)
        is_np = True
    else:
        inputs_ = inputs.copy()
        is_np = False

    inputs_['hh'] = inputs_['high'].rolling(period).max()
    inputs_['lc'] = inputs_['close'].rolling(period).min()
    inputs_['hc'] = inputs_['close'].rolling(period).max()
    inputs_['ll'] = inputs_['low'].rolling(period).min()
    inputs_['range'] = np.maximum(inputs_['hh'] - inputs_['lc'], inputs_['hc'] - inputs_['ll'])
    inputs_['buy_line'] = inputs_['open'] + k1 * inputs_['range']
    inputs_['sell_line'] = inputs_['open'] - k2 * inputs_['range']
    if is_np:
        return [inputs_['buy_line'].values, inputs_['sell_line'].values]
    else:
        return inputs_[['buy_line', 'sell_line']]


def EATR(inputs, ema_period=14):
    tr = TRANGE(inputs)
    return EMA(tr, ema_period)


def SUPERTREND(inputs, multipler: float, eatr_period=14):
    eatr = EATR(inputs, eatr_period)
    if isinstance(inputs, dict):
        inputs_ = pd.DataFrame(inputs)
        is_np = True
    else:
        inputs_ = inputs.copy()
        is_np = False
    mid = (inputs_['high'] + inputs_['low']) / 2
    basic_upper_band = mid + multipler * eatr
    basic_lower_band = mid - multipler * eatr

    final_upper_band = basic_upper_band.values
    final_lower_band = basic_lower_band.values
    for i in range(1, len(final_upper_band)):
        if np.isnan(final_upper_band[i]) is False:
            if basic_upper_band[i] < final_upper_band[i - 1]:
                final_upper_band[i] = basic_upper_band[i]
            elif inputs['close'][i - 1] > final_upper_band[i - 1]:
                final_upper_band[i] = basic_upper_band[i]
            else:
                final_upper_band[i] = final_upper_band[i - 1]

        if np.isnan(final_lower_band[i]) is False:
            if basic_lower_band[i] > final_lower_band[i - 1]:
                final_lower_band[i] = basic_lower_band[i]
            elif inputs['close'][i - 1] < final_lower_band[i - 1]:
                final_lower_band[i] = basic_lower_band[i]
            else:
                final_lower_band[i] = final_lower_band[i - 1]

    if is_np:
        return [final_lower_band, final_upper_band]
    else:
        return pd.DataFrame({'final_lower': final_lower_band, 'final_upper': final_upper_band}, index=inputs_.index)


def MAMOM_CLIP(inputs, period: int = 2, price_type: str = 'MA-10'):
    indicator = MOM(inputs, period, price_type=price_type)
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    indicator = np.clip(indicator, -5, 5)
    return indicator


def SECONDARY_MOM(inputs, period: int = 2, price_type: str = 'close'):
    pass


def hpfilter(X, lamb=1600):
    X = np.asarray(X, float)
    if X.ndim > 1:
        X = X.squeeze()
    nobs = len(X)
    I = sparse.eye(nobs, nobs)
    offsets = np.array([0, 1, 2])
    data = np.repeat([[1.], [-2.], [1.]], nobs, axis=1)
    K = sparse.dia_matrix((data, offsets), shape=(nobs - 2, nobs))
    use_umfpack = True
    trend = spsolve(I + lamb * K.T.dot(K), X, use_umfpack=use_umfpack)
    cycle = X - trend
    return trend, cycle


if __name__ == '__main__':
    inputs = {
        'open': np.random.random(100),
        'high': np.random.random(100),
        'low': np.random.random(100),
        'close': np.random.random(100),
        'volume': np.random.random(100)
    }
    eatr = EATR(inputs, 14)
    st = SUPERTREND(inputs, 0.1)
