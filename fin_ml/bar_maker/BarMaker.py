import os
import pandas as pd
import numpy as np


class BarMaker:
    def __init__(self, tick_df: pd.DataFrame):
        self.tick = tick_df

    def make_time_bar(self, time_interval: str):
        pass

    def make_count_bar(self, count: int):
        pass

    def make_volume_bar(self, vol: int):
        pass

    def make_dollar_bar(self):
        pass

    def make_imbalanced_bar(self, alpha: float):
        pass

    def make_run_bar(self):
        pass

    def make_customized_bar(self):
        pass


class TickBarMaker(BarMaker):
    def __init__(self, tick_df: pd.DataFrame,
                 time_key='DateTime',
                 bid_key='Bid',
                 ask_key='Ask',
                 volume_key=None,
                 last_price=None,
                 mp_key=None,
                 bid_vol_key=None,
                 ask_vol_key=None,
                 time_key_format='%m/%d/%Y %H:%M:%S.%f'):
        super().__init__(tick_df)
        self.time_key = time_key
        self.bid_key = bid_key
        self.ask_key = ask_key
        self.volume_key = volume_key
        self.last_price = last_price
        self.mp_key = mp_key
        self.bid_vol = bid_vol_key
        self.ask_vol = ask_vol_key
        self.price_key = ''
        if last_price is not None:
            self.price_key = last_price
        elif mp_key is not None:
            self.price_key = mp_key
        else:
            self.tick['mp'] = (self.tick[bid_key] + self.tick[ask_key]) / 2
            self.price_key = 'mp'
        cols = [self.time_key, self.price_key]
        if self.volume_key is not None:
            cols.append(self.volume_key)
        self.tick_data = self.tick[cols]
        self.tick_data[self.time_key] = pd.to_datetime(self.tick_data[self.time_key], format=time_key_format)
        self.tick_data.set_index(self.time_key, inplace=True)

    def make_time_bar(self, interval: str):
        bar_data = self.tick_data.copy()
        resampler = bar_data.resample(interval)
        agg_dict = {self.price_key: ['ohlc', 'count']
                    }

        bar_data = resampler.agg(agg_dict)  # type: pd.DataFrame
        bar_data.columns = bar_data.columns.get_level_values(2)
        bar_data.rename(columns={'mp': 'count'}, inplace=True)
        bar_data.fillna(method='ffill', inplace=True)
        if self.volume_key is not None:
            bar_data[self.volume_key] = resampler.agg({self.volume_key: 'sum'})
        return bar_data

    def make_count_bar(self, count: int):
        count_bar = self.tick_data.copy()
        count_bar['c'] = 1
        count_bar['c'] = count_bar['c'].cumsum().floordiv(count)
        agg_dict = {self.price_key: 'ohlc',
                    self.time_key: 'max'
                    }
        if self.volume_key is not None:
            agg_dict[self.volume_key] = 'sum'

        count_bar = count_bar.reset_index().groupby('c').agg(agg_dict)
        count_bar.columns = count_bar.columns.get_level_values(1)
        count_bar.set_index(self.time_key, inplace=True)
        count_bar['count'] = count
        return count_bar

    def make_imbalanced_bar(self, alpha: float, default_T: int = 10):
        # todo possible wrong implementation
        T = []
        bar_sampled_event = [self.tick_data.index[0]]
        pro_b1_bar_list = []

        df = self.tick_data.copy()
        df['bt'] = df['mp'].diff()
        df['bt'] = df['bt'].abs() / df['bt']
        df['bt'] = np.where(df['bt'] == 0, df['bt'].shift(1), df['bt'])
        df['bt'] = df['bt'].fillna(0)
        df['group'] = 0
        group = 0

        cur = default_T
        while cur < len(self.tick_data) - 1:
            # break_condition = False
            if group == 0:
                b1_count = np.sum(np.where(df['bt'].values[:default_T] == 1, 1, 0)) + df['bt'].values[default_T - 1]
                pro_b1 = b1_count / default_T
                bar_sampled_event.append(self.tick_data.index[default_T])
                T.append(default_T)
                pro_b1_bar_list.append(pro_b1)
                df['group'].loc[bar_sampled_event[-2]:bar_sampled_event[-1]] = group
                group += 1
            else:
                expected_T = (T[-1] - T[-2]) * alpha + T[-2] if len(T) > 1 else T[-1]
                expected_pro_b1 = (pro_b1_bar_list[-1] - pro_b1_bar_list[-2]) * alpha + pro_b1_bar_list[-2] \
                    if len(pro_b1_bar_list) > 1 else pro_b1_bar_list[-1]
                theta = 0
                b1_count = 0
                t_temple = 0
                cur = sum(T)
                threshold = expected_T * abs(2 * expected_pro_b1 - 1)

                while abs(theta) < threshold and cur < len(self.tick_data) - 1:
                    b = df['bt'].values[cur]
                    theta += b
                    if b == 1:
                        b1_count += 1
                    cur += 1
                    t_temple += 1
                T.append(t_temple)
                bar_sampled_event.append(self.tick_data.index[cur])
                pro_b1 = b1_count / t_temple
                pro_b1_bar_list.append(pro_b1)
                df['group'].loc[bar_sampled_event[-2]:bar_sampled_event[-1]] = group
                group += 1

        agg_dict = {self.price_key: 'ohlc',
                    self.time_key: 'last'
                    }

        grouper = df.reset_index().groupby('group')
        bar_data = grouper.agg(agg_dict)

        bar_data.columns = bar_data.columns.get_level_values(1)
        bar_data['count'] = grouper.agg({self.price_key: 'count'})
        if self.volume_key is not None:
            bar_data[self.volume_key] = grouper.agg({self.volume_key: 'sum'})
        return bar_data

    def make_run_bar(self):
        pass


class BarBarMaker(BarMaker):

    def __init__(self, tick_df: pd.DataFrame,
                 time_key='DateTime',
                 ohlc_key=None,
                 volume_key=None,
                 time_key_format='%m/%d/%Y %H:%M:%S.%f',
                 bid_prefix='Bid',
                 ask_prefix='Ask',
                 tickqty = None
                 ):
        super(BarBarMaker, self).__init__(tick_df)
        self.time_key = time_key
        self.volume_key = volume_key
        self.time_key_format = time_key_format
        self.bid_prefix = bid_prefix
        self.ask_prefix = ask_prefix
        self.tickqty = tickqty
        if ohlc_key is None:
            self.ohlc_key = ['Open', 'High', 'Low', 'Close']
        else:
            self.ohlc_key = ohlc_key
        for col in self.ohlc_key:
            self.tick[col] = (self.tick[self.bid_prefix + col] + self.tick[self.ask_prefix + col]) / 2
        cols = [self.time_key]
        cols.extend(self.ohlc_key)
        if self.volume_key is not None:
            cols.append(self.volume_key)
        self.bar_data = self.tick[cols]
        self.bar_data[self.time_key] = pd.to_datetime(self.bar_data[self.time_key], format=time_key_format)
        self.bar_data.set_index(self.time_key, inplace=True)


    def make_time_bar(self, time_interval: str):
        bar_data = self.bar_data.copy()
        resampler = bar_data.resample(time_interval)
        agg_dict = {self.ohlc_key[0]: 'first',
                    self.ohlc_key[1]: 'max',
                    self.ohlc_key[2]: 'min',
                    self.ohlc_key[3]: 'last',
                    }
        bar_data = resampler.agg(agg_dict)  # type: pd.DataFrame

        if self.volume_key is not None:
            bar_data[self.volume_key] = resampler.agg({self.volume_key: 'sum'})
        return bar_data

    def make_count_bar(self, count: int):
        if self.tickqty is None:
            raise KeyError()
        pass


if __name__ == '__main__':
    # tick_df = pd.read_csv(r'../../local_data/EURUSD/tick/EURUSD_2016_1.csv')

    # bm = TickBarMaker(tick_df)

    # time_bar = bm.make_time_bar('1H')
    # count_bar = bm.make_count_bar(100)
    # imbalance = bm.make_imbalanced_bar(0.5)

    min_bar_df = pd.read_csv(r'../../local_data/EURUSD/m1/EURUSD_m1_2019_2.csv')
    bm = BarBarMaker(min_bar_df)
