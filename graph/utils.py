import pandas as pd


def timestamp_parser(series, timestamp):
    if timestamp is None:
        timestamp = series.index
        timestamp = timestamp.strftime('%Y/%m/%d %H:%M:%S')
    elif isinstance(timestamp, pd.Series):
        timestamp = timestamp.apply(lambda x: pd.Timestamp.strftime(x, '%Y/%m/%d %H:%M:%S'))

    return timestamp
