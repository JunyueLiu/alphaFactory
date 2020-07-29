import os
import pandas as pd

def merge_single_asset(paths, time_key='Date', code_key = 'code'):
    dfs = []
    for p in paths:
        df = pd.read_csv(p)
        dfs.append(df)
    merged = pd.concat(dfs)
    merged.set_index([time_key, code_key], inplace=True)
    merged.columns = [c.lower() for c in merged.columns]
    merged.sort_index(inplace=True)
    return merged

if __name__ == '__main__':
    files = os.listdir(r'../local_data')
    paths = [os.path.join(r'../local_data', f) for f in files]
    df = merge_single_asset(paths)
    df.to_csv(r'../hsi_component.csv')