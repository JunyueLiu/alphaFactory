# TRIPLE - BARRIER LABELING METHOD
import pandas as pd
import numpy as np
def TBL(df,barrier,width):
    upwidth,downwidth = width
    barrier_ = barrier
    result = barrier_[['code','time_key','vb']].copy(deep=True)

    if upwidth>0:
        barrier_['ub'] = upwidth*barrier_['volume']
    else:
        barrier_['ub'] = np.nan
    if downwidth>0:
        barrier_['db'] = -downwidth*barrier_['volume']
    else:
        barrier_['db'] = np.nan
    for code in barrier_.code.unique():
        barrier0 = barrier_[barrier_.code == code]
        print(barrier0)
        for col,time_key,vb in barrier_[['time_key','vb']].itertuples():
            df0 = df[(df.time_key>time_key) & (df.time_key<vb)]
            df0['return'] = df0['close']/df[df.time_key==time_key]['close'].iloc[0]-1
            result.loc[result.index[(result.time_key==time_key) & (result.code==code)],'ut'] = \
            df0[df0['return']>barrier0[barrier0.time_key==time_key]['ub'].iloc[0]]['time_key'].min()
            result.loc[result.index[(result.time_key==time_key) & (result.code==code)],'dt'] = \
            df0[df0['return']<barrier0[barrier0.time_key==time_key]['db'].iloc[0]]['time_key'].min()
    return result
def get_first_touch(df,barrier,width,minvolume):
    #barrier = [barrier.volume>minvolume]
    result = TBL(df,barrier,width)
    result['first'] = result[['vb','ut','dt']].dropna(how='all').min(axis=1)
    return result

def get_bins(result,df):
    result = result.dropna(subset=['first'])
    out = result[['code','time_key']]
    barprice = pd.merge(result,df,on=['code','time_key'],how='left')['close']
    touchprice = pd.merge(result,df,left_on=['code','first'],right_on=['code','time_key'],how='left')['close']
    out['ret'] = touchprice/barprice-1
    out['bin'] = np.sign(out['ret'])
    return out
if __name__ == '__main__':
    df = pd.read_csv(r'../../data.csv')
    df = df[:500]
    df['time_key'] = pd.to_datetime(df['time_key'])
    df['vb'] = pd.to_datetime(df['time_key']+pd.Timedelta(minutes=15))
    # width：一个包含两个非负值的list，分别为上限barrier和下限barrier与估计波动率vol相乘的因子
    width = [1,1]
    #minvolume 我没用minvolume判断
    result = get_first_touch(df,df,width,-1)
    out = get_bins(result,df)
    #最后bin是标签
    print(out)
