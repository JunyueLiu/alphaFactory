import pandas as pd
import numpy as np


def normalize_factor(factor: pd.DataFrame, mean=None, std=None):
    if mean is None:
        mean = factor.mean()
    if std is None:
        mean = factor.std()
    return (factor - mean) / std


def sigmoid(factor: pd.DataFrame):
    s = 1 / (1 + np.exp(- factor.values))
    return pd.DataFrame(s, index=factor.index)

