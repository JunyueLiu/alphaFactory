from alpha_research.factor_zoo.utils import *
import pandas as pd
data = pd.read_csv(r'../../hsi_component.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index(['Date', 'code'], inplace=True)
close_ = data['close']
volume_ = data['volume']
open_ = data['open']


