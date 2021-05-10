import datetime
import os
import pandas as pd
import threading

import pytz
import tqdm
from arctic import Arctic, arctic
from arctic.date import DateRange
from arctic.exceptions import LibraryNotFoundException, NoDataFoundException

from fin_ml.bar_maker.BarMaker import BarBarMaker, TickBarMaker


def tick_1min_count_bar(tick_df: pd.DataFrame,
                        count: int,
                        name: str,
                        mode: str = 'arctic',
                        save_folder: str or None = None,
                        arctic_store: Arctic or None = None
                        ):
    bm = TickBarMaker(tick_df, time_key='index')

    time_bar = bm.make_time_bar('1T')
    time_bar.reset_index(inplace=True)

    bm2 = BarBarMaker(time_bar, time_key='date', ohlc_key=['open', 'high', 'low', 'close'],
                      time_key_format='%Y-%m-%d %H:%M:%S', bid_prefix=None, ask_prefix=None)
    count_bar = bm2.make_count_bar(count)
    count_bar['code'] = name.split('_')[0]
    count_bar['k_type'] = 'K_' + str(count) + 'count'
    if mode == 'csv':
        if save_folder is None:
            raise KeyError('save_folder must provide for csv mode')
        count_bar.to_csv(os.path.join(save_folder, name), float_format='%.5f')
    elif mode == 'arctic':
        if arctic_store is None:
            raise KeyError('arctic_store must provide for arctic mode')
        try:
            lib = arctic_store.get_library('{}count'.format(count))
        except LibraryNotFoundException:
            arctic_store.initialize_library('{}count'.format(count), lib_type=arctic.VERSION_STORE)
            lib = arctic_store.get_library('{}count'.format(count))
        lib.append(name, count_bar, prune_previous_version=False, upsert=True)


def get_all_count_bar_from_arctic(count: int, name: str, arctic_store : Arctic, year_start=2016, year_end=None):
    today = datetime.datetime.now()
    if year_end is None:
        year_end = today.year

    for i in tqdm.tqdm(range(year_start, year_end + 1)):
        for j in range(1, 54):
            mkt_open = datetime.datetime.strptime("{}-W{}-1 17:00:00".format(i, j), "%Y-W%W-%w %H:%M:%S")
            mkt_open = pytz.timezone('US/Eastern').localize(mkt_open)
            mkt_close = datetime.datetime.strptime("{}-W{}-5 17:00:00".format(i, j), "%Y-W%W-%w %H:%M:%S")
            mkt_close = pytz.timezone('US/Eastern').localize(mkt_close)
            if mkt_open.year > i:
                continue
            lib = arctic_store.get_library('tick')
            # todo
            try:
                tick_df = lib.read(name, date_range=DateRange(mkt_open, mkt_close))
                tick_1min_count_bar(tick_df, count, name, 'arctic', arctic_store=store)
            except NoDataFoundException:
                print('empty: {} {}'.format(mkt_open, mkt_close))



def batch_barbar_making(tick_data_folder, count, save_folder, year=None):
    if os.path.exists(save_folder) is False:
        os.makedirs(save_folder)

    tick_paths = os.listdir(tick_data_folder)
    if year is not None:
        tick_paths = [p for p in tick_paths if filter_year(p, year)]

    for path in tqdm.tqdm(tick_paths):
        tick_1min_count_bar(os.path.join(tick_data_folder, path), count, save_folder, path)
        print('finish...', path)
    print('finish')


def filter_year(name, year):
    y = int(name.split('_')[1])
    if y == year:
        return True
    else:
        return False


if __name__ == '__main__':
    # tick_data_folder = r'../../local_data/EURUSD/tick/'
    # save_folder = r'../../local_data/EURUSD/count5000/'
    # batch_barbar_making(tick_data_folder, 5000, save_folder)
    store = Arctic('localhost')
    # tick_df = store['tick'].read('EUR/USD', _target_tick_count=10)
    # tick_1min_count_bar(tick_df, 2000, 'EUR/USD', 'arctic', arctic_store=store)
    get_all_count_bar_from_arctic(12000, 'USD/JPY', store)