import numpy as np
import pandas as pd
from technical_analysis.overlap import *
from technical_analysis.volatility import *
from technical_analysis.volume import *
from technical_analysis.momentum import *
from technical_analysis.pattern import *
from technical_analysis.customization import *
from technical_analysis.utils import MA_Type


class BarManager:

    def __init__(self, bar_name, size=100, ta_parameters=None):
        self.size = size
        self.inited = False
        self.interval = None
        self.bar_name = bar_name

        self.time = np.zeros(size)
        self.open = np.zeros(size)
        self.high = np.zeros(size)
        self.low = np.zeros(size)
        self.close = np.zeros(size)
        self.volume = np.zeros(size)
        self.technical_indicator_parameters = None
        self.ta = None  # to store technical indicators
        self.customized_indicator_name = []

        self._set_technical_indicator(ta_parameters)
        self.max_TI_period = 0

    def init_with_pandas(self, data, time_key=None, ohlcv_key=None):
        if ohlcv_key is None:
            ohlcv_key = ['open', 'high', 'low', 'close', 'volume']

        if isinstance(data, pd.DataFrame) is False:
            raise ValueError('This method has to initial with pandas object')

        if time_key is None:
            self.time = np.array(data.index[:self.size], dtype='datetime64')
        else:
            self.time = np.array(data[time_key][:self.size], dtype='datetime64')

        self.open = data[ohlcv_key[0]].values[-self.size:]
        self.high = data[ohlcv_key[1]].values[-self.size:]
        self.low = data[ohlcv_key[2]].values[-self.size:]
        self.close = data[ohlcv_key[3]].values[-self.size:]
        try:
            self.volume = data[ohlcv_key[4]].values[-self.size:]
        except:
            print('no volume in the columns')
        self.inited = True
        self._calculate_ta(True)

    def update_with_pandas(self, row, time_key=None, ohlcv_key=None):
        if ohlcv_key is None:
            ohlcv_key = ['open', 'high', 'low', 'close', 'volume']

        if isinstance(row, pd.DataFrame) is False:
            raise ValueError('This method has to initial with pandas object')

        if time_key is None:
            time = np.array(row.index, dtype='datetime64')
        else:
            time = np.array(row[time_key], dtype='datetime64')

        # to support uncompleted bar
        if time[-1] > self.time[-1]:
            # new bar coming in, move the nparray for the new bar
            self.time[0: self.size - 1] = self.time[1: self.size]
            self.open[0: self.size - 1] = self.open[1: self.size]
            self.high[0: self.size - 1] = self.high[1: self.size]
            self.low[0: self.size - 1] = self.low[1: self.size]
            self.close[0: self.size - 1] = self.close[1: self.size]
            self.volume[0: self.size - 1] = self.volume[1: self.size]
            self.time[-1] = time[-1]

        self.open[-1] = row[ohlcv_key[0]].values[-1]
        self.high[-1] = row[ohlcv_key[1]].values[-1]
        self.low[-1] = row[ohlcv_key[2]].values[-1]
        self.close[-1] = row[ohlcv_key[3]].values[-1]
        try:
            self.volume[-1] = row[ohlcv_key[4]].values[-1]
        except:
            print('no volume in the columns')
        self._calculate_ta()

    def _set_technical_indicator(self, ta_parameter):
        ta_setting = ta_parameter[self.bar_name]
        self.technical_indicator_parameters = ta_setting

    def _calculate_ta(self, init=False):
        if self.technical_indicator_parameters is None:
            return

        if init:
            inputs = {
                'open': self.open,
                'high': self.high,
                'low': self.low,
                'close': self.close,
                'volume': self.volume,
                # 'periods': np.random.random(100)
            }
            if 'periods' in self.__dict__:
                inputs['periods'] = self.__dict__['periods']

            self.ta = {}
            for key, value in self.technical_indicator_parameters.items():
                call_string = ''
                for para, v in value.items():
                    if para == 'indicator':
                        call_string += v
                        call_string += '(inputs'
                    else:
                        str_v = str(v)
                        call_string = call_string + ',' + para + '=' + str_v
                        if para == 'period' and v > self.max_TI_period:
                            self.max_TI_period = v
                call_string += ')'
                indicator = eval(call_string)
                self.ta[key] = indicator

            # to make sure that maximum technical indicator calculation period is not 0
            if self.max_TI_period == 0:
                self.max_TI_period = self.size
        else:
            inputs = {
                'open': self.open[-self.max_TI_period:],
                'high': self.high[-self.max_TI_period:],
                'low': self.low[-self.max_TI_period:],
                'close': self.close[-self.max_TI_period:],
                'volume': self.volume[-self.max_TI_period:],
            }
            if 'periods' in self.__dict__:
                inputs['periods'] = self.__dict__['periods'][-self.max_TI_period:]
            for key, value in self.technical_indicator_parameters.items():
                call_string = ''
                for para, v in value.items():
                    if para == 'indicator':
                        call_string += v
                        call_string += '(inputs'
                    else:
                        str_v = str(v)
                        call_string = call_string + ',' + para + '=' + str_v
                call_string += ')'
                indicator = eval(call_string)[-1]
                self.ta[key][0: self.size - 1] = self.ta[key][1:]
                self.ta[key][-1] = indicator

    def add_customized_indicator(self, name, data):
        if len(data) != self.size:
            raise ValueError('Have to have the same size with bar data, which is {})'.format(self.size))
        self.customized_indicator_name.append(name)
        self.__dict__[name] = data

    def update_customized_indicator(self, name, data):
        self.__dict__[name][0: self.size - 1] = self.__dict__[name][1:]
        self.__dict__[name][-1] = data

    def to_pandas(self):
        data = self.to_dictionary()
        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)
        return df

    def to_dictionary(self):
        data = {'timestamp': self.time,
                'open': self.open,
                'high': self.high,
                'low': self.low,
                'close': self.close,
                'volume': self.volume}
        for key, value in self.ta.items():
            data['ta_' + key] = value
        for name in self.customized_indicator_name:
            data[name] = self.__dict__[name]
        return data


if __name__ == '__main__':
    ta_par = {
        "K_1M": {
            "MA1": {
                "indicator": "MA",
                "period": 5
            },
            "MA2": {
                "indicator": "MA",
                "period": 10,
                "matype": 'MA_Type.SMA',
                "price_type": "\'close\'"
            }
        },
        "K_3M": {
        }
    }
    df = pd.read_csv(
        '/Users/liujunyue/PycharmProjects/ljquant/hkex_data/HK.800000_2019-02-25 09:30:00_2020-02-21 16:00:00_K_1M_qfq.csv')
    bar_manager = BarManager('K_1M', 100, ta_par)
    bar_manager.init_with_pandas(df[:100], time_key='time_key')
    bar_manager.update_with_pandas(df[100:101], time_key='time_key')
    bar_manager.add_customized_indicator('all_one', np.arange(100))
    bar_manager.to_pandas()
