import os
from futu import *


def download_kline_and_save(futu_context: OpenQuoteContext, code,
                      start_time=None, end_time=None,
                      klinetype=KLType.K_DAY,
                      autype=AuType.QFQ, save_folder=''):
    df_list = []

    ret, data, page_req_key = \
        futu_context.request_history_kline(code, start=start_time,
                                           end=end_time, ktype=klinetype, autype=autype)
    if ret != RET_OK:
        raise ValueError

    df_list.append(data)

    while page_req_key is not None:
        ret, data, page_req_key = \
            futu_context.request_history_kline(code, start=start_time,
                                               end=end_time, ktype=klinetype, autype=autype, page_req_key=page_req_key)

        if ret != RET_OK:
            raise ValueError
        print('fetching......')
        df_list.append(data)

    df = pd.concat(df_list)
    start = str(df['time_key'].values[0])
    end = str(df['time_key'].values[-1])

    path = os.path.join(save_folder, '{}_{}_{}_{}_{}.csv'.format(code, start, end, klinetype, autype))
    df.to_csv(path, index=False)
    print('finish download: {}_{}_{}_{}_{}'.format(code, start, end, klinetype, autype))
