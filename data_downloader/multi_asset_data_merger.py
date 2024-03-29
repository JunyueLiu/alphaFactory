import os
import pandas as pd
import tqdm

def merge_single_asset(paths, time_key='Date', code_key = 'code') -> pd.DataFrame:
    dfs = []
    for p in tqdm.tqdm(paths):
        df = pd.read_csv(p)
        dfs.append(df)
    merged = pd.concat(dfs)
    merged[code_key] = merged[code_key].apply(lambda x: x.split('.')[0])
    merged[time_key] = pd.to_datetime(merged[time_key])
    merged.set_index([time_key, code_key], inplace=True)
    merged.columns = [c.lower() for c in merged.columns]
    merged.sort_index(inplace=True)
    return merged

if __name__ == '__main__':
    files = os.listdir(r'../local_data')
    paths = [os.path.join(r'../local_data', f) for f in files]
    df = merge_single_asset(paths)
    df.to_csv(r'../hsi_component.csv')