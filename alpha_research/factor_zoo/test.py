from alpha_research.factor_zoo.utils import *
from alpha_research.factor_zoo.alpha_101 import *
import pandas as pd
if __name__ == '__main__':
    data = pd.read_csv(r'../../hsi_component.csv')

    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'code'], inplace=True)
    # print(data)
    # close_ = data['close']
    # volume_ = data['volume']
    # open_ = data['open']
    print(alpha_11(data))

