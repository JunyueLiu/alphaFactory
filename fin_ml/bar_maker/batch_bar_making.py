import os
import pandas as pd
import threading
import tqdm
from fin_ml.bar_maker.BarMaker import BarBarMaker, TickBarMaker


def tick_1min_count_bar(tick_csv_path: str, count: int, save_folder: str, name: str):
    tick_df = pd.read_csv(tick_csv_path)

    bm = TickBarMaker(tick_df)

    time_bar = bm.make_time_bar('1T')
    time_bar.reset_index(inplace=True)

    bm2 = BarBarMaker(time_bar, time_key='date', ohlc_key=['open', 'high', 'low', 'close'],
                      time_key_format='%Y-%m-%d %H:%M:%S', bid_prefix=None, ask_prefix=None)
    count_bar = bm2.make_count_bar(count)
    count_bar['code'] = name.split('_')[0]
    count_bar['k_type'] = 'K_' + str(count) + 'count'
    count_bar.to_csv(os.path.join(save_folder, name),float_format='%.5f')


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
    tick_data_folder = r'../../local_data/EURUSD/tick/'
    save_folder = r'../../local_data/EURUSD/count5000/'
    batch_barbar_making(tick_data_folder, 5000, save_folder)
