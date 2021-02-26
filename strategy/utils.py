import numpy as np


def bull_ratio(close_arr, ma_arr, days):
    return np.sum(ma_arr[-days:] < close_arr[-days:]) / days


def bear_ratio(close_arr, ma_arr, days):
    return np.sum(ma_arr[-days:] > close_arr[-days:]) / days


def indicators_filter(close, indicators: list, long: bool):
    if long is True:
        return np.all(np.array(indicators) >= close)
    else:
        return np.all(np.array(indicators) <= close)


def trend_continuity(indicator, look_back: list, long: bool):
    if long is True:
        count = 0
        for i in range(1, len(look_back)):
            if indicator[-look_back[i - 1]] >= indicator[-look_back[i]]:
                count += 1
        return count / len(look_back)
    else:
        count = 0
        for i in range(1, len(look_back)):
            if indicator[-look_back[i - 1]] <= indicator[-look_back[i]]:
                count += 1
        return count / len(look_back)


def trend_consensus():
    pass
