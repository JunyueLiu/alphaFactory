from scipy import sparse
from scipy.sparse.linalg import spsolve

from technical_analysis.momentum import MOM
from technical_analysis import utils
import numpy as np
import pandas as pd

__func__ = [
    'DUALTHRUST',
    'MAMOM_CLIP',
    'SECONDARY_MOM'

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
