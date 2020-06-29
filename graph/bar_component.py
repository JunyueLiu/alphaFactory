from plotly import graph_objects as go
import pandas as pd


def candlestick(df: pd.DataFrame, timestamp=None, ohlc_key=None, symbol=None,
                increasing_line_color=None, decreasing_line_color=None,
                text=None, textposition=None):
    if ohlc_key is None:
        ohlc_key = ['open', 'high', 'low', 'close']
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))

    return go.Candlestick(x=timestamp,
                          open=df[ohlc_key[0]],
                          high=df[ohlc_key[1]],
                          low=df[ohlc_key[2]],
                          close=df[ohlc_key[3]], name=symbol,
                          increasing_line_color=increasing_line_color,
                          decreasing_line_color=decreasing_line_color)


def ohlc(df: pd.DataFrame, timestamp=None, ohlc_key=None, symbol=None,
         increasing_line_color=None, decreasing_line_color=None, strftime_str='%Y/%m/%d %H:%M:%S'):
    if ohlc_key is None:
        ohlc_key = ['open', 'high', 'low', 'close']
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime(strftime_str)
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, strftime_str))
    return go.Ohlc(x=timestamp,
                   open=df[ohlc_key[0]],
                   high=df[ohlc_key[1]],
                   low=df[ohlc_key[2]],
                   close=df[ohlc_key[3]], name=symbol,
                   increasing_line_color=increasing_line_color,
                   decreasing_line_color=decreasing_line_color)


def time_sharing_chart(df: pd.DataFrame, timestamp=None, price_key=None, symbol=None):
    if price_key is None:
        price_key = 'price'
    if timestamp is None:
        timestamp = df.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    if isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))
    return go.Scatter(x=timestamp, y=df[price_key], name=symbol, )
