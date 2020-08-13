import json
import pandas as pd

pd.set_option('max_columns', None)


def read_orderbook_json(path: str) -> list:
    records = []
    with open(path, 'r') as file:
        for line in file.readlines():
            dic = json.loads(line)
            records.append(dic)
    return records


def get_orderbook_df(path: str) -> pd.DataFrame:
    return pd.DataFrame(read_orderbook_json(path))


if __name__ == '__main__':
    # df = pd.read_json('2020-07-31.json')
    records = []
    with open('2020-07-31.json', 'r') as file:
        for line in file.readlines():
            dic = json.loads(line)
            records.append(dic)
    df = pd.DataFrame(records)
    sample = {'_id': {'$oid': '5f22eac623de44d2b46056ce'},
              'code': 'HK.999010',
              'svr_recv_time_bid': '2020-07-30 23:44:06.596',
              'svr_recv_time_ask': '2020-07-30 23:44:06.596',
              'Bid': [[24476.0, 1, 1],
                      [24475.0, 4, 3],
                      [24474.0, 2, 2],
                      [24473.0, 4, 4],
                      [24472.0, 3, 3],
                      [24471.0, 2, 2],
                      [24470.0, 8, 3],
                      [24469.0, 3, 3],
                      [24468.0, 2, 2],
                      [24467.0, 3, 3]],
              'Ask': [[24477.0, 1, 1],
                      [24478.0, 2, 2],
                      [24479.0, 4, 4],
                      [24480.0, 2, 2],
                      [24481.0, 4, 4],
                      [24482.0, 3, 3],
                      [24483.0, 5, 5],
                      [24484.0, 4, 4],
                      [24485.0, 7, 5],
                      [24486.0, 3, 3]]}
