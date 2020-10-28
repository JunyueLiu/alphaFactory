from bs4 import BeautifulSoup
import pandas as pd
import time
import tqdm


def download_csi300_history_component():
    df = pd.read_html('http://stock.jrj.com/share,sz399300,nlscf.shtml')[-1]
    for i in tqdm.trange(2, 37):
        df1 = pd.read_html('http://stock.jrj.com/share,sz399300,nlscf_' + str(i) + '.shtml')[-1]
        df = df.append(df1)
        # time.sleep(0.5)

    df = df.append(pd.read_html('http://stock.jrj.com/share,sz399300,nzxcf.shtml')[-1])
    for i in tqdm.trange(2, 15):
        df1 = pd.read_html('http://stock.jrj.com/share,sz399300,nzxcf_' + str(i) + '.shtml')[-1]
        df = df.append(df1)
        # time.sleep(0.5)
    df['股票代码'] = df['股票代码'].apply(lambda x: str(x))
    df['股票代码'] = df['股票代码'].apply(lambda x: x if len(x) == 6 else '0' * (6 - len(x)) + x)
    df.rename(columns={'股票代码': 'code', '纳入时间': 'in_time', '剔除时间': 'out_time'}, inplace=True)
    df = df[['code', 'in_time', 'out_time']]
    df = df.drop_duplicates().set_index('code').sort_index() # type:pd.DataFrame
    df.to_parquet('csi300_component.parquet')

if __name__ == '__main__':
    download_csi300_history_component()