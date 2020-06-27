"""
Aim to contain some studied factor in the literature

"""
import pandas as pd
import numpy as np
from scipy import stats
from alpha_research.factor_zoo.utils import *


def alpha_1(df: pd.DataFrame):
    """
    Alpha#1: (rank(Ts_ArgMax(SignedPower(((returns < 0) ? stddev(returns, 20) : close), 2.), 5)) - 0.5)
    :return:
    """
    pass


def alpha_2(df: pd.DataFrame):
    """
    Alpha#2: (-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))
    :param df:
    :return:
    """
    pass


def alpha_3(df: pd.DataFrame):
    """
    Alpha#3: (-1 * correlation(rank(open), rank(volume), 10))
    :param df:
    :return:
    """
    pass


def alpha_4(df: pd.DataFrame):
    """
    Alpha#4: (-1 * Ts_Rank(rank(low), 9))
    :param df:
    :return:
    """
    pass


def alpha_5(df: pd.DataFrame):
    """
    Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap)))))
    :param df:
    :return:
    """
    pass


def alpha_6(df: pd.DataFrame, time_lag=10):
    """
    Alpha#6: (-1 * correlation(open, volume, 10))
    :param df:
    :param time_lag:
    :return:
    """

    factor = -1 * correlation(df['open'], df['volume'], time_lag)
    return factor


def alpha_7(df: pd.DataFrame):
    """
    Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1))
    :param df:
    :return:
    """
    pass


def alpha_8(df: pd.DataFrame):
    """
    Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))

    :param df:
    :return:
    """

    pass


def alpha_9(df: pd.DataFrame, time_shift=1, rolling_windows=5):
    """
    Alpha#9: ((0 < ts_min(delta(close, 1), 5)) ? delta(close, 1) : ((ts_max(delta(close, 1), 5) < 0) ? delta(close, 1) : (-1 * delta(close, 1))))
    :param df:
    :param time_shift:
    :param rolling_windows:
    :return:
    """
    condition = (df['close'] - df['close'].shift(time_shift)).rolling(rolling_windows).min()
    condition2 = (df['close'] - df['close'].shift(time_shift)).rolling(rolling_windows).max()
    ans1 = df['close'] - df['close'].shift(1)
    factor = np.where(condition > 0, ans1, np.where(condition2 < 0, ans1, -1 * ans1))
    # print(factor)
    return factor


def alpha_10(df: pd.DataFrame):
    """
    Alpha#10: rank(((0 < ts_min(delta(close, 1), 4)) ? delta(close, 1) : ((ts_max(delta(close, 1), 4) < 0) ? delta(close, 1) : (-1 * delta(close, 1)))))
    :param df:
    :return:
    """
    pass


def alpha_11(df: pd.DataFrame):
    """
    Alpha#11:((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))
    :param df:
    :return:
    """
    pass


def alpha_12(df: pd.DataFrame, time_lag=1):
    """

    Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1)))
    :param df:
    :param time_lag:
    :return:
    """

    factor = np.sign(df['volume'] - df['volume'].shift(1)) * (-1 * (df['close'] - df['close'].shift(1)))
    # print(factor)
    return factor


def alpha_13(df: pd.DataFrame):
    """
    Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5)))

    :param df:
    :return:
    """
    pass


def alpha_14(df: pd.DataFrame):
    """
    Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))
    :param df:
    :return:
    """
    pass


def alpha_15(df: pd.DataFrame):
    """
    Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))
    :param df:
    :return:
    """

    pass


def alpha_16(df: pd.DataFrame):
    """
    Alpha#16: (-1 * rank(covariance(rank(high), rank(volume), 5)))
    :param df:
    :return:
    """
    pass


def alpha_17(df: pd.DataFrame):
    """
    Alpha#17: (((-1 * rank(ts_rank(close, 10))) * rank(delta(delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5)))
    :param df:
    :return:
    """
    pass


def alpha_18(df: pd.DataFrame):
    """
    Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))
    :param df:
    :return:
    """
    pass


def alpha_19(df: pd.DataFrame):
    """
    Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))
    :param df:
    :return:
    """
    pass


def alpha_20(df: pd.DataFrame):
    """
    Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))

    :param df:
    :return:
    """

    pass


def alpha_21(df: pd.DataFrame):
    """
    ((((sum(close, 8) / 8) + stddev(close, 8)) < (sum(close, 2) / 2)) ?
    (-1 * 1) : (((sum(close, 2) / 2) < ((sum(close, 8) / 8) - stddev(close, 8))) ? 1 : (((1 < (volume / adv20)) || ((volume / adv20) == 1)) ? 1 : (-1 * 1))))
    :param df:
    :return:
    """
    condition1 = df['close'].rolling(8).mean() + df['close'].rolling(8).std()
    condition2 = df['close'].rolling(2).mean()
    condition3 = df['close'].rolling(8).mean() - df['close'].rolling(8).std()
    condition4 = df['volume'] / df['volume'].rolling(20).mean()
    factor = np.where(condition1 < condition2, -1,
                      np.where(condition2 < condition3, 1, np.where(condition4 >= 1, 1, -1)))
    # print(factor)
    return factor


def alpha_22(df: pd.DataFrame):
    """

    Alpha#22: (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))
    :param df:
    :return:
    """
    pass


def alpha_23(df: pd.DataFrame, time_lag=20):
    """
    Alpha#23: (((sum(high, 20) / 20) < high) ? (-1 * delta(high, 2)) : 0)
    :param df:
    :param time_lag:
    :return:
    """
    tmp = df['high'].rolling(time_lag).mean()
    factor = np.where(df['high'] > tmp, -1 * (df['high'] - df['high'].shift(2)), 0)
    return factor


def alpha_24(df: pd.DataFrame):
    """
    Alpha#24: ((((delta((sum(close, 100) / 100), 100) / delay(close, 100)) < 0.05) || ((delta((sum(close, 100) / 100), 100) / delay(close, 100)) == 0.05)) ? (-1 * (close - ts_min(close, 100))) : (-1 * delta(close, 3)))
    :param df:
    :return:
    """
    delta_sum = df['close'].rolling(100).mean()
    delta_sum = delta_sum - delta_sum.shift(100)
    delay_close = df['close'].shift(100)
    tmp1 = delta_sum / delay_close
    ts_min = df['close'].rolling(100).min()
    factor = np.where(tmp1 <= 0.05, df['close'] - ts_min, df['close'] - df['close'].shift(3))
    return factor


def alpha_25(df: pd.DataFrame):
    """
    Alpha#25: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))

    :param df:
    :return:
    """

    pass


def alpha_26(df: pd.DataFrame):
    """
    Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))
    :param df:
    :return:
    """
    factor = []
    return factor


def alpha_27(df: pd.DataFrame):
    """
    Alpha#27: ((0.5 < rank((sum(correlation(rank(volume), rank(vwap), 6), 2) / 2.0))) ? (-1 * 1) : 1)
    :param df:
    :return:
    """
    pass


def alpha_28(df: pd.DataFrame):
    """
    Alpha#28: scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))
    :param df:
    :return:
    """
    pass
    factor = []
    return factor


def alpha_29(df: pd.DataFrame):
    """
    Alpha#29: (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))

    :param df:
    :return:
    """

    pass


def alpha_30(df: pd.DataFrame):
    """
    Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))

    :param df:
    :return:
    """
    pass


def alpha_31(df: pd.DataFrame):
    """
    Alpha#31: ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 * delta(close, 3)))) + sign(scale(correlation(adv20, low, 12))))
    :param df:
    :return:
    """
    pass


def alpha_32(df: pd.DataFrame):
    """
    Alpha#32: (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5), 230))))

    :param df:
    :return:
    """
    factor = []
    return factor


def alpha_33(df: pd.DataFrame):
    """
    Alpha#33: rank((-1 * ((1 - (open / close))^1)))
    :param df:
    :return:
    """
    pass


def alpha_34(df: pd.DataFrame):
    """
    Alpha#34: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))
    :param df:
    :return:
    """
    pass


def alpha_35(df: pd.DataFrame):
    """
    Alpha#35: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32)))
    :param df:
    :return:
    """
    factor = []
    return factor


def alpha_36(df: pd.DataFrame):
    """
    Alpha#36: (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open - close)))) + (0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap, adv20, 6)))) + (0.6 * rank((((sum(close, 200) / 200) - open) * (close - open)))))
    :param df:
    :return:
    """
    pass


def alpha_37(df: pd.DataFrame):
    """

    Alpha#37: (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))
    :param df:
    :return:
    """
    pass


def alpha_38(df: pd.DataFrame):
    """
    Alpha#38: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open)))
    :param df:
    :return:
    """
    pass


def alpha_39(df: pd.DataFrame):
    """
    Alpha#39: ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 + rank(sum(returns, 250))))
    :param df:
    :return:
    """
    pass


def alpha_40(df: pd.DataFrame):
    """
    Alpha#40: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))
    :param df:
    :return:
    """
    pass


def alpha_41(df: pd.DataFrame):
    """
    Alpha#41: (((high * low)^0.5) - vwap)
    :param df:
    :return:
    """
    vwap = (np.cumsum(df['volume'] * df['close']) / np.cumsum(df['volume']))
    factor = np.power(df['high'] * df['low'], 0.5) - vwap
    return factor


def alpha_42(df: pd.DataFrame):
    """
    Alpha#42: (rank((vwap - close)) / rank((vwap + close)))
    :param df:
    :return:
    """
    _vwap = vwap(df['close'], df['volume'])
    _close = df['close']
    return rank(_vwap - _close) / rank(_vwap + _close)


def alpha_43(df: pd.DataFrame):
    """
    Alpha#43: (ts_rank((volume / adv20), 20) * ts_rank((-1 * delta(close, 7)), 8))
    :param df:
    :return:
    """
    # todo
    pass
    tmp1 = df['volume'] / df['volume'].rolling(20).mean()
    rank1 = tmp1.rank()
    rank2 = -1 * (df['close'] - df['close'].shift(7)).rank()


def alpha_44(df: pd.DataFrame):
    """
    Alpha#44: (-1 * correlation(high, rank(volume), 5))

    :param df:
    :return:
    """
    pass


def alpha_45(df: pd.DataFrame):
    """
    Alpha#45: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) * rank(correlation(sum(close, 5), sum(close, 20), 2))))
    :param df:
    :return:
    """
    pass


def alpha_46(df: pd.DataFrame):
    """
    Alpha#46: ((0.25 < (((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10))) ? (-1 * 1) : (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < 0) ? 1 : ((-1 * 1) * (close - delay(close, 1)))))
    :param df:
    :return:
    """

    condition = (df['close'].shift(20) - df['close'].shift(10)) / 10 - (df['close'].shift(10) - df['close']) / 10
    factor = np.where(condition > 0.25, -1, np.where(condition < 0, 1, -1 * (df['close'] - df['close'].shift(1))))
    return factor


def alpha_47(df: pd.DataFrame):
    """
    Alpha#47: ((((rank((1 / close)) * volume) / adv20) * ((high * rank((high - close))) / (sum(high, 5) / 5))) - rank((vwap - delay(vwap, 5))))
    :param df:
    :return:
    """
    pass


def alpha_48(df: pd.DataFrame):
    """
    Alpha#48: (indneutralize(((correlation(delta(close, 1), delta(delay(close, 1), 1), 250) * delta(close, 1)) / close), IndClass.subindustry) / sum(((delta(close, 1) / delay(close, 1))^2), 250))
    :param df:
    :return:
    """
    pass


def alpha_49(df: pd.DataFrame):
    """
    Alpha#49: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 * 0.1)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))

    :param df:
    :return:
    """
    condition = (df['close'].shift(20) - df['close'].shift(10)) / 10 - (df['close'].shift(10) - df['close']) / 10
    factor = np.where(condition < -0.1, 1, (-1 * (df['close'] - df['close'].shift(1))))
    return factor


def alpha_50(df: pd.DataFrame):
    """

    Alpha#50: (-1 * ts_max(rank(correlation(rank(volume), rank(vwap), 5)), 5))
    :param df:
    :return:
    """
    pass


def alpha_51(df: pd.DataFrame):
    """

Alpha#51: (((((delay(close, 20) - delay(close, 10)) / 10) - ((delay(close, 10) - close) / 10)) < (-1 * 0.05)) ? 1 : ((-1 * 1) * (close - delay(close, 1))))
    :param df:
    :return:
    """
    condition = (df['close'].shift(20) - df['close'].shift(10)) / 10 - (df['close'].shift(10) - df['close']) / 10
    factor = np.where(condition < -0.05, 1, -1 * (df['close'] - df['close'].shift(1)))
    return factor


def alpha_52(df: pd.DataFrame):
    """
    Alpha#52: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) - sum(returns, 20)) / 220))) * ts_rank(volume, 5))

    :param df:
    :return:
    """
    pass


def alpha_53(df: pd.DataFrame):
    """
    Alpha#53: (-1 * delta((((close - low) - (high - close)) / (close - low)), 9))
    :param df:
    :return:
    """

    tmp = (df['close'] - df['low']) / (df['close'] - df['low'])
    factor = -1 * (tmp - tmp.shift(9))
    return factor


def alpha_54(df: pd.DataFrame):
    """
    Alpha#54: ((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5)))
    :param df:
    :return:
    """
    factor = (-1 * ((df['low'] - df['close']) * np.power(df['open'], 5)) / (
            (df['low'] - df['high']) * np.power(df['close'], 5)))
    # print(factor)
    return factor


def alpha_55(df: pd.DataFrame):
    """
    Alpha#55: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6))
    :param df:
    :return:
    """

    pass


def alpha_56(df: pd.DataFrame):
    """
    Alpha#56: (0 - (1 * (rank((sum(returns, 10) / sum(sum(returns, 2), 3))) * rank((returns * cap)))))
    :param df:
    :return:
    """

    pass


def alpha_57(df: pd.DataFrame):
    """
    Alpha#57: (0 - (1 * ((close - vwap) / decay_linear(rank(ts_argmax(close, 30)), 2))))
    :param df:
    :return:
    """

    pass


def alpha_58(df: pd.DataFrame):
    """

    Alpha#58: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322))

    :param df:
    :return:
    """

    pass


def alpha_59(df: pd.DataFrame):
    """
    Alpha#59: (-1 * Ts_Rank(decay_linear(correlation(IndNeutralize(((vwap * 0.728317) + (vwap * (1 - 0.728317))), IndClass.industry), volume, 4.25197), 16.2289), 8.19648))
    :param df:
    :return:
    """
    pass


def alpha_60(df: pd.DataFrame):
    """
    Alpha#60: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - scale(rank(ts_argmax(close, 10))))))
    :param df:
    :return:
    """
    pass


def alpha_61(df: pd.DataFrame):
    """
    Alpha#61: (rank((vwap - ts_min(vwap, 16.1219))) < rank(correlation(vwap, adv180, 17.9282)))
    :param df:
    :return:
    """

    pass


def alpha_62(df: pd.DataFrame):
    """
    Alpha#62: ((rank(correlation(vwap, sum(adv20, 22.4101), 9.91009)) < rank(((rank(open) + rank(open)) < (rank(((high + low) / 2)) + rank(high))))) * -1)
    :param df:
    :return:
    """

    pass


def alpha_63(df: pd.DataFrame):
    """
    Alpha#63: ((rank(decay_linear(delta(IndNeutralize(close, IndClass.industry), 2.25164), 8.22237)) - rank(decay_linear(correlation(((vwap * 0.318108) + (open * (1 - 0.318108))), sum(adv180, 37.2467), 13.557), 12.2883))) * -1)

    :param df:
    :return:
    """

    pass


def alpha_64(df: pd.DataFrame):
    """
    Alpha#64: ((rank(correlation(sum(((open * 0.178404) + (low * (1 - 0.178404))), 12.7054), sum(adv120, 12.7054), 16.6208)) < rank(delta(((((high + low) / 2) * 0.178404) + (vwap * (1 - 0.178404))), 3.69741))) * -1)

    :param df:
    :return:
    """
    pass


def alpha_65(df: pd.DataFrame):
    """
    Alpha#65: ((rank(correlation(((open * 0.00817205) + (vwap * (1 - 0.00817205))), sum(adv60, 8.6911), 6.40374)) < rank((open - ts_min(open, 13.635)))) * -1)
    :param df:
    :return:
    """
    pass


def alpha_66(df: pd.DataFrame):
    """
    Alpha#66: ((rank(decay_linear(delta(vwap, 3.51013), 7.23052)) + Ts_Rank(decay_linear(((((low * 0.96633) + (low * (1 - 0.96633))) - vwap) / (open - ((high + low) / 2))), 11.4157), 6.72611)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_67(df: pd.DataFrame):
    """
    Alpha#67: ((rank((high - ts_min(high, 2.14593)))^rank(correlation(IndNeutralize(vwap, IndClass.sector), IndNeutralize(adv20, IndClass.subindustry), 6.02936))) * -1)

    :param df:
    :return:
    """

    pass


def alpha_68(df: pd.DataFrame):
    """
    Alpha#68: ((Ts_Rank(correlation(rank(high), rank(adv15), 8.91644), 13.9333) < rank(delta(((close * 0.518371) + (low * (1 - 0.518371))), 1.06157))) * -1)
    :param df:
    :return:
    """
    pass


def alpha_69(df: pd.DataFrame):
    """
    Alpha#69: ((rank(ts_max(delta(IndNeutralize(vwap, IndClass.industry), 2.72412), 4.79344))^Ts_Rank(correlation(((close * 0.490655) + (vwap * (1 - 0.490655))), adv20, 4.92416), 9.0615)) * -1)
    :param df:
    :return:
    """
    # SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close, 4.96796))
    return


def alpha_70(df: pd.DataFrame):
    """
    Alpha#70: ((rank(delta(vwap, 1.29456))^Ts_Rank(correlation(IndNeutralize(close, IndClass.industry), adv50, 17.8256), 17.9171)) * -1)

    :param df:
    :return:
    """
    pass


def alpha_71(df: pd.DataFrame):
    """
    Alpha#71: max(Ts_Rank(decay_linear(correlation(Ts_Rank(close, 3.43976), Ts_Rank(adv180, 12.0647), 18.0175), 4.20501), 15.6948), Ts_Rank(decay_linear((rank(((low + open) - (vwap + vwap)))^2), 16.4662), 4.4388))
    :param df:
    :return:
    """
    pass


def alpha_72(df: pd.DataFrame):
    """
    Alpha#72: (rank(decay_linear(correlation(((high + low) / 2), adv40, 8.93345), 10.1519)) / rank(decay_linear(correlation(Ts_Rank(vwap, 3.72469), Ts_Rank(volume, 18.5188), 6.86671), 2.95011)))

    :param df:
    :return:
    """
    pass


def alpha_73(df: pd.DataFrame):
    """
    Alpha#73: (max(rank(decay_linear(delta(vwap, 4.72775), 2.91864)), Ts_Rank(decay_linear(((delta(((open * 0.147155) + (low * (1 - 0.147155))), 2.03608) / ((open * 0.147155) + (low * (1 - 0.147155)))) * -1), 3.33829), 16.7411)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_74(df: pd.DataFrame):
    """
    Alpha#74: ((rank(correlation(close, sum(adv30, 37.4843), 15.1365)) < rank(correlation(rank(((high * 0.0261661) + (vwap * (1 - 0.0261661)))), rank(volume), 11.4791))) * -1)
    :param df:
    :return:
    """
    pass


def alpha_75(df: pd.DataFrame):
    """

    Alpha#75: (rank(correlation(vwap, volume, 4.24304)) < rank(correlation(rank(low), rank(adv50), 12.4413)))

    :param df:
    :return:
    """
    pass


def alpha_76(df: pd.DataFrame):
    """

    Alpha#76: (max(rank(decay_linear(delta(vwap, 1.24383), 11.8259)), Ts_Rank(decay_linear(Ts_Rank(correlation(IndNeutralize(low, IndClass.sector), adv81, 8.14941), 19.569), 17.1543), 19.383)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_77(df: pd.DataFrame):
    """

    Alpha#77: min(rank(decay_linear(((((high + low) / 2) + high) - (vwap + high)), 20.0451)), rank(decay_linear(correlation(((high + low) / 2), adv40, 3.1614), 5.64125)))
    :param df:
    :return:
    """
    pass


def alpha_78(df: pd.DataFrame):
    """
    Alpha#78: (rank(correlation(sum(((low * 0.352233) + (vwap * (1 - 0.352233))), 19.7428), sum(adv40, 19.7428), 6.83313))^rank(correlation(rank(vwap), rank(volume), 5.77492)))
    :param df:
    :return:
    """
    pass


def alpha_79(df: pd.DataFrame):
    """
    Alpha#79: (rank(delta(IndNeutralize(((close * 0.60733) + (open * (1 - 0.60733))), IndClass.sector), 1.23438)) < rank(correlation(Ts_Rank(vwap, 3.60973), Ts_Rank(adv150, 9.18637), 14.6644)))

    :param df:
    :return:
    """
    pass


def alpha_80(df: pd.DataFrame):
    """
    Alpha#80: ((rank(Sign(delta(IndNeutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545)))^Ts_Rank(correlation(high, adv10, 5.11456), 5.53756)) * -1)

    :param df:
    :return:
    """
    pass


def alpha_81(df: pd.DataFrame):
    """
    Alpha#81: ((rank(Log(product(rank((rank(correlation(vwap, sum(adv10, 49.6054), 8.47743))^4)), 14.9655))) < rank(correlation(rank(vwap), rank(volume), 5.07914))) * -1)

    :param df:
    :return:
    """
    pass


def alpha_82(df: pd.DataFrame):
    """
    Alpha#82: (min(rank(decay_linear(delta(open, 1.46063), 14.8717)), Ts_Rank(decay_linear(correlation(IndNeutralize(volume, IndClass.sector), ((open * 0.634196) + (open * (1 - 0.634196))), 17.4842), 6.92131), 13.4283)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_83(df: pd.DataFrame):
    """
    Alpha#83: ((rank(delay(((high - low) / (sum(close, 5) / 5)), 2)) * rank(rank(volume))) / (((high - low) / (sum(close, 5) / 5)) / (vwap - close)))
    :param df:
    :return:
    """
    pass


def alpha_84(df: pd.DataFrame):
    """
    Alpha#84: SignedPower(Ts_Rank((vwap - ts_max(vwap, 15.3217)), 20.7127), delta(close, 4.96796))

    :param df:
    :return:
    """
    pass


def alpha_85(df: pd.DataFrame):
    """
    Alpha#85: (rank(correlation(((high * 0.876703) + (close * (1 - 0.876703))), adv30, 9.61331))^rank(correlation(Ts_Rank(((high + low) / 2), 3.70596), Ts_Rank(volume, 10.1595), 7.11408)))
    :param df:
    :return:
    """
    pass


def alpha_86(df: pd.DataFrame):
    """
    Alpha#86: ((Ts_Rank(correlation(close, sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open + close) - (vwap + open)))) * -1)
    :param df:
    :return:
    """
    pass


def alpha_87(df: pd.DataFrame):
    """
    Alpha#87: (max(rank(decay_linear(delta(((close * 0.369701) + (vwap * (1 - 0.369701))), 1.91233), 2.65461)), Ts_Rank(decay_linear(abs(correlation(IndNeutralize(adv81, IndClass.industry), close, 13.4132)), 4.89768), 14.4535)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_88(df: pd.DataFrame):
    """
    Alpha#88: min(rank(decay_linear(((rank(open) + rank(low)) - (rank(high) + rank(close))), 8.06882)), Ts_Rank(decay_linear(correlation(Ts_Rank(close, 8.44728), Ts_Rank(adv60, 20.6966), 8.01266), 6.65053), 2.61957))
    :param df:
    :return:
    """
    pass


def alpha_89(df: pd.DataFrame):
    """

    Alpha#89: (Ts_Rank(decay_linear(correlation(((low * 0.967285) + (low * (1 - 0.967285))), adv10, 6.94279), 5.51607), 3.79744) - Ts_Rank(decay_linear(delta(IndNeutralize(vwap, IndClass.industry), 3.48158), 10.1466), 15.3012))
    :param df:
    :return:
    """
    pass


def alpha_90(df: pd.DataFrame):
    """
    Alpha#90: ((rank((close - ts_max(close, 4.66719)))^Ts_Rank(correlation(IndNeutralize(adv40, IndClass.subindustry), low, 5.38375), 3.21856)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_91(df: pd.DataFrame):
    """
    Alpha#91: ((Ts_Rank(decay_linear(decay_linear(correlation(IndNeutralize(close, IndClass.industry), volume, 9.74928), 16.398), 3.83219), 4.8667) - rank(decay_linear(correlation(vwap, adv30, 4.01303), 2.6809))) * -1)
    :param df:
    :return:
    """
    pass


def alpha_92(df: pd.DataFrame):
    """
    Alpha#92: min(Ts_Rank(decay_linear(((((high + low) / 2) + close) < (low + open)), 14.7221), 18.8683), Ts_Rank(decay_linear(correlation(rank(low), rank(adv30), 7.58555), 6.94024), 6.80584))

    :param df:
    :return:
    """
    pass


def alpha_93(df: pd.DataFrame):
    """

    Alpha#93: (Ts_Rank(decay_linear(correlation(IndNeutralize(vwap, IndClass.industry), adv81, 17.4193), 19.848), 7.54455) / rank(decay_linear(delta(((close * 0.524434) + (vwap * (1 - 0.524434))), 2.77377), 16.2664)))
    :param df:
    :return:
    """
    pass


def alpha_94(df: pd.DataFrame):
    """
    Alpha#94: ((rank((vwap - ts_min(vwap, 11.5783)))^Ts_Rank(correlation(Ts_Rank(vwap, 19.6462), Ts_Rank(adv60, 4.02992), 18.0926), 2.70756)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_95(df: pd.DataFrame):
    """
    Alpha#95: (rank((open - ts_min(open, 12.4105))) < Ts_Rank((rank(correlation(sum(((high + low) / 2), 19.1351), sum(adv40, 19.1351), 12.8742))^5), 11.7584))

    :param df:
    :return:
    """
    pass


def alpha_96(df: pd.DataFrame):
    """
    Alpha#96: (max(Ts_Rank(decay_linear(correlation(rank(vwap), rank(volume), 3.83878), 4.16783), 8.38151), Ts_Rank(decay_linear(Ts_ArgMax(correlation(Ts_Rank(close, 7.45404), Ts_Rank(adv60, 4.13242), 3.65459), 12.6556), 14.0365), 13.4143)) * -1)
    :param df:
    :return:
    """
    pass


def alpha_97(df: pd.DataFrame):
    """
    Alpha#97: ((rank(decay_linear(delta(IndNeutralize(((low * 0.721001) + (vwap * (1 - 0.721001))), IndClass.industry), 3.3705), 20.4523)) - Ts_Rank(decay_linear(Ts_Rank(correlation(Ts_Rank(low, 7.87871), Ts_Rank(adv60, 17.255), 4.97547), 18.5925), 15.7152), 6.71659)) * -1)
    :param df:
    :return:
    """

    pass


def alpha_98(df: pd.DataFrame):
    """
    Alpha#98: (rank(decay_linear(correlation(vwap, sum(adv5, 26.4719), 4.58418), 7.18088)) - rank(decay_linear(Ts_Rank(Ts_ArgMin(correlation(rank(open), rank(adv15), 20.8187), 8.62571), 6.95668), 8.07206)))

    :param df:
    :return:
    """
    pass


def alpha_99(df: pd.DataFrame):
    """

    Alpha#99: ((rank(correlation(sum(((high + low) / 2), 19.8975), sum(adv60, 19.8975), 8.8136)) < rank(correlation(low, volume, 6.28259))) * -1)

    :param df:
    :return:
    """

    pass


def alpha_100(df: pd.DataFrame):
    """
    Alpha#100: (0 - (1 * (((1.5 * scale(indneutralize(indneutralize(rank(((((close - low) - (high - close)) / (high - low)) * volume)), IndClass.subindustry), IndClass.subindustry))) - scale(indneutralize((correlation(close, rank(adv20), 5) - rank(ts_argmin(close, 30))), IndClass.subindustry))) * (volume / adv20))))
    :param df:
    :return:
    """
    pass


def alpha_101(df: pd.DataFrame):
    """
    Alpha#101: ((close - open) / ((high - low) + .001))
    :param df:
    :return:
    """
    factor = (df['close'] - df['open']) / ((df['high'] - df['low']) + 0.001)
    # print(factor)
    return factor


if __name__ == '__main__':
    df = pd.read_csv('../data.csv').head(200)
    # print(alpha_6(df))
    alpha_21(df)
