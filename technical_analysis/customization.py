from technical_analysis.momentum import MOM
from technical_analysis import utils
import numpy as np

__func__ = [
    'MAMOM_CLIP',
    'SECONDARY_MOM'

]


def MAMOM_CLIP(inputs, period: int = 2, price_type: str = 'MA-10'):
    indicator = MOM(inputs, period, price_type=price_type)
    if not utils.check(inputs, [price_type]):
        raise ValueError('')
    indicator = np.clip(indicator, -5, 5)
    return indicator


def SECONDARY_MOM(inputs, period: int = 2, price_type: str = 'close'):
    pass
