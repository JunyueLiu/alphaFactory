from alpha_research.factor_zoo.utils import *
from alpha_research.factor_zoo.alpha_101 import *
import pandas as pd
import yfinance as yf

if __name__ == '__main__':

    # test phase 1 single asset
    hsi = yf.Ticker("^HSI")
    hsi = hsi.history(period="7d", interval='1m')
    hsi.index = hsi.index.tz_localize(None)
    hsi.columns = [c.lower() for c in hsi.columns]













    data = pd.read_csv(r'../../hsi_component.csv')

    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index(['Date', 'code'], inplace=True)

    print(alpha_11(data))

