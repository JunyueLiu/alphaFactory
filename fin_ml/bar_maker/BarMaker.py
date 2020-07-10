import pandas as pd
import os


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
        agg_dict = {self.price_key: ['ohlc', 'count'],
                    }
        if self.volume_key is not None:
            agg_dict[self.volume_key] = 'sum'

        bar_data = resampler.agg(agg_dict)  # type: pd.DataFrame
        bar_data.fillna(method='ffill', inplace=True)
        bar_data.columns = bar_data.columns.get_level_values(2)
        bar_data.rename(columns={'mp': 'count'}, inplace=True)
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

    def make_imbalanced_bar(self, alpha: float):
        pass

    def make_run_bar(self):
        pass




if __name__ == '__main__':
    tick_df = pd.read_csv(r'../../local_data/EURUSD/tick/EURUSD_2016_1.csv')
    bm = TickBarMaker(tick_df)
    # time_bar = bm.make_time_bar('1H')
    count_bar = bm.make_count_bar(100)