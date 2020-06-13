import pandas as pd
import numpy as np


def normalize_factor(factor: pd.DataFrame, mean=None, std=None) -> pd.DataFrame:
    if mean is None:
        mean = factor.mean()
    if std is None:
        mean = factor.std()
    return (factor - mean) / std


def sigmoid(factor: pd.DataFrame) -> pd.DataFrame:
    s = 1 / (1 + np.exp(- factor.values))
    return pd.DataFrame(s, index=factor.index)


def percentile_factor(factor: pd.DataFrame, percentage: float) -> pd.Series:
    percent_factor = factor.fillna(0)
    eighty = np.percentile(percent_factor, percentage * 100)
    twenty = np.percentile(percent_factor, (1 - percentage) * 100)
    percent = np.where(percent_factor.values >= eighty,
                       1, np.where(percent_factor.values <= twenty, -1, 0))
    percent_factor = pd.Series(percent, index=factor.index)
    return percent_factor
