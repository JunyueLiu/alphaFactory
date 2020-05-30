import pandas as pd
import plotly
from graph.indicator_component import *
from graph.bar_component import *
from graph.stock_graph import *
from technical_analysis.overlap import MA
from technical_analysis.volatility import ATR
from technical_analysis.momentum import MOM

if __name__ == '__main__':
    df = pd.read_csv('/Users/liujunyue/PycharmProjects/ljquant/hkex_data/HK.800000_2019-02-25 09:30:00_2020-02-21 16:00:00_K_1M_qfq.csv')

    df['time_key'] = pd.to_datetime(df['time_key'])
    df = df[df['time_key'] >= pd.to_datetime('2020-02-20')]
    df = df[df['time_key'] <= pd.to_datetime('2020-02-21')]
    df['ma5'] = MA(df, 5)
    df['ma10'] = MA(df, 10)
    df['ma20'] = MA(df, 20)
    # df['atr'] = ATR(df)
    # df['mom'] = MOM(df, 5)
    df['mom_ma10'] = MOM(df, 2, price_type='ma10')
    # df['mom_ma10'] = np.clip(df['mom_ma10'], -5, 5)
    df['mom_ma20'] =MOM(df, 2, price_type='ma20')
    # df['mom_ma20'] = np.clip(df['mom_ma20'], -5, 5)
    df['diff'] = MOM(df, 1, 'mom_ma10')
    # df['diff_diff'] = MOM(df, 1, price_type='diff')


    kline = candlestick(df, df['time_key'],symbol='HSI')
    # fig = stick_and_volume(kline,
    #                  volume(df, df['time_key'], 'turnover'))
    # # fig.show()
    # plotly.offline.plot(fig, filename='file.html')
    #
    # fig1 = stick_overlap_indicator(kline, band3(df, df['time_key'], ['ma5', 'ma10', 'ma20']))
    # plotly.offline.plot(fig1, filename='file1.html')

    # fig2 = stick_and_nonoverlap_indicators(kline, no_overlap(df, df['time_key'], ['atr']))
    # plotly.offline.plot(fig2, filename='file2.html')
    indicators = no_overlap(df, df['time_key'], ['ma5', 'ma10', 'ma20', 'mom_ma10','mom_ma20','diff'])

    fig = stick_and_indicators(kline, indicators, [0,0,0, 1,1,1])
    plotly.offline.plot(fig, filename='test.html')

