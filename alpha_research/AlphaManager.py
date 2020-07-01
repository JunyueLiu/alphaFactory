from db_wrapper.mongodb_utils import MongoConnection
from alpha_research.factor_zoo.alpha_101 import *
from alpha_research.SingleAssetResearch import *
import pandas as pd
import pickle
import traceback

# from db_wrapper.mongodb_utils import *

HK = 'HK'
CHINA = 'CN'
US = 'US'
EUROPE = 'EU'
JAPAN = 'JP'


# 把函数放入list 直接把函数名称append进去就好了 https://www.cnblogs.com/xudashu/p/3831600.html


class AlphaStorage:
    def __init__(self, name: str,
                 alpha_function,  # can be defined using the liquidity profile, such as TOP50, TOP100, TOP200, TOP1500
                 alpha_parameter: dict,
                 alpha_idea: str,
                 alpha_regions: str or list,
                 alpha_universe: str or list,  # index
                 performance_parameter: dict):
        self.name = name
        self.alpha_function = pickle.dumps(alpha_function)  # use pickle.loads() transfer back

        self.alpha_parameter = alpha_parameter
        # alpha_parameter dict {'select_parameter':{'para1': var1, 'para2': var1, ...},
        #                   'parameter_range': {'para1': {'type': 'int', 'range':[]},
        #                   'para2': {'type': float, 'range':[]}
        #                   , ...},}
        self.alpha_idea = alpha_idea
        self.alpha_regions = alpha_regions
        self.alpha_universe = alpha_universe
        self.performance_parameter = performance_parameter
        # performance_parameter
        # [{'data': '有可能是一条数据库的query语句 "db|collection|index_start|index_end"
        # selection query or somehow identify the data from the dataset'
        # 'performance':{
        # 一个dict
        # }}]




    def to_dict(self):
        # turn object to dict
        return vars(self)

    def get_alpha_function(self):
        return pickle.loads(self.alpha_function)

    def get_alpha_parameter(self):
        return pickle.loads(self.alpha_parameter)

    def get_performance_paremeter(self):
        return pickle.loads(self.performance_parameter)




class AlphaManager():

    def __init__(self, connect: MongoConnection):
        self.mongo_con = connect


    def add_alpha(self, db: str, collection: str, alpha_storage: AlphaStorage):
        try:
            result = self.mongo_con.client[db][collection].insert(AlphaStorage.to_dict(alpha_storage))
            print(result)
        except Exception:
            traceback.print_exc()

    def query_alpha(self, db: str, collection: str, query: dict):
        try:
            result = self.mongo_con.client[db][collection].find(query)
            # return as dict list
            alphaStorage_list = []
            for alphaStorage in result:
                alphaStorage_list.append(self.transfer_dict_to_MongoConnection(alphaStorage))
            return alphaStorage_list
        except Exception:
            traceback.print_exc()

    def transfer_dict_to_MongoConnection(self,input_dict:dict) ->MongoConnection:

        alphaStorage = AlphaStorage(input_dict['name'],
                                    pickle.loads(input_dict['alpha_function']),
                                    input_dict['alpha_parameter'],
                                    input_dict['alpha_idea'],
                                    input_dict['alpha_regions'],
                                    input_dict['alpha_universe'],
                                    input_dict['performance_parameter'])
        return alphaStorage


    def query_alpha_by_datasets(self, datasets: str):

        pass

    def alpha_vs_alpha(self):
        pass


if __name__ == '__main__':
    #sample data
    data_path = r'HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'
    df = pd.read_csv(data_path)
    df['time_key'] = pd.to_datetime(df['time_key'])
    df.set_index('time_key', inplace=True)
    data = df[-100:]

    # factor_study = SingleAssetResearch(df)
    # factor = factor_study.calculate_factor(alpha_6, **{'time_lag': 5})
    # func = alpha_6


    # connect mongodb
    connect = MongoConnection('120.55.45.12', 27017, 'root', 'AlphaFactory2020')
    alpha_storage = AlphaStorage('test', alpha_6, {'selected': {'para1': 1},
                                                   'parameter_range': {'para1': {'type': 'int'
                                                                    #eval('int') transfer string to type int
                                                       , 'range': [1, 2]}}},
                                 'test',
                                 CHINA, 'CSI300', {'data': data})
    db = 'test'
    collection = 'alphatest'
    manager = AlphaManager(connect)
    manager.add_alpha(db, collection, alpha_storage)
    query = {'name': 'test'}
    alphaStorage_list = manager.query_alpha(db,collection,query)

    # 返回是一个list list中每个对象是dict




