from db_wrapper.mongodb_utils import MongoConnection
from alpha_research.factor_zoo.alpha_101 import *
from alpha_research.SingleAssetResearch import *
import pandas as pd
import pickle
import inspect
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
        if isinstance(alpha_function, str):
            self.alpha_function = alpha_function
        elif hasattr(alpha_function, '__call__'):
            self.alpha_function = inspect.getsource(alpha_function)
        else:
            raise ValueError('alpha_function must be string or function type')

        self.alpha_parameter = alpha_parameter
        # alpha_parameter dict {'select_parameter':{'para1': var1, 'para2': var1, ...},
        #                   'parameter_range': {'para1': {'type': 'int', 'range':[]},
        #                   'para2': {'type': float, 'range':[]}
        #                   , ...},}
        self.alpha_idea = alpha_idea
        if isinstance(alpha_universe, str):
            self.alpha_universe = [alpha_universe]
        else:
            self.alpha_universe = alpha_universe

        if isinstance(alpha_regions, str):
            self.alpha_regions = [alpha_regions]
        else:
            self.alpha_regions = alpha_regions

        self.performance_parameter = performance_parameter

    def to_dict(self):
        # turn object to dict
        dic = vars(self)

        if isinstance(dic['performance_parameter']['data'], pd.DataFrame):
            dic['performance_parameter']['data'] = dic['performance_parameter']['data'].to_json()

        return dic

    def get_alpha_function(self):
        return self.alpha_function

    def get_alpha_parameter(self):
        return self.alpha_parameter

    def get_performance_parameter(self):
        return self.performance_parameter


class AlphaManager:

    def __init__(self, connect: MongoConnection):
        self.mongo_con = connect

    def add_alpha(self, db: str, collection: str, alpha_storage: AlphaStorage):
        try:
            result = self.mongo_con.client[db][collection].insert_one(AlphaStorage.to_dict(alpha_storage))
            # print(result)
        except Exception:
            traceback.print_exc()

    def query_alpha(self, db: str, collection: str, query: dict):
        try:
            results = self.mongo_con.client[db][collection].find(query)
            # return as dict list
            alphaStorage_list = []
            for res in results:
                alphaStorage_list.append(self.from_dict_to_alphaStorage(res))
            return alphaStorage_list
        except Exception:
            traceback.print_exc()

    def from_dict_to_alphaStorage(self, input_dict: dict) -> AlphaStorage:
        alphaStorage = AlphaStorage(input_dict['name'],
                                    input_dict['alpha_function'],
                                    input_dict['alpha_parameter'],
                                    input_dict['alpha_idea'],
                                    input_dict['alpha_regions'],
                                    input_dict['alpha_universe'],
                                    input_dict['performance_parameter'])
        return alphaStorage

    def query_alpha_by_datasets(self, db, collection,
                                datasets: str or pd.DataFrame):
        if isinstance(datasets, pd.DataFrame):
            datasets = datasets.to_json()
        alpha_storage_list = self.query_alpha(db, collection, {'performance_parameter': {'data': datasets}})
        return alpha_storage_list

    def query_alpha_by_alpha_name(self, db: str, collection: str,
                                  alpha_name: str):
        alpha_storage_list = self.query_alpha(db, collection, {'name': alpha_name})
        return alpha_storage_list

    def query_alpha_by_universe(self, db: str, collection: str, universe: str or list):
        if isinstance(universe, str):
            universe = [universe]
        alpha_storage_list = self.query_alpha(db, collection, {"alpha_universe": {"$all": universe}})
        return alpha_storage_list

    def query_alpha_by_regions(self, db: str, collection: str, regions: str):
        if isinstance(regions, str):
            regions = [regions]
        alpha_storage_list = self.query_alpha(db, collection, {"alpha_regions": {"$all": regions}})
        return alpha_storage_list

    def query_alpha_by_alpha_idea(self, db: str, collection: str, idea: str):
        alpha_storage_list = self.query_alpha(db, collection, {"alpha_idea": {"$regex": '.*' + idea + '.*'}})
        return alpha_storage_list

    def alpha_vs_alpha(self, alpha_db_id):
        pass



# todo:添加时间，作者
# 查的时候可以查出alpha有多少
if __name__ == '__main__':
    # sample data
    # data_path = r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'
    # df = pd.read_csv(data_path)
    # df['time_key'] = pd.to_datetime(df['time_key'])
    # df.set_index('time_key', inplace=True)
    # data = df[-100:]

    # factor_study = SingleAssetResearch(df)
    # factor = factor_study.calculate_factor(alpha_6, **{'time_lag': 5})
    # func = alpha_6

    # connect mongodb
    connect = MongoConnection('120.55.45.12', 27017, 'root', 'AlphaFactory2020')
    # print('connect')
    # alpha_storage = AlphaStorage('alpha_1', alpha_1, {},
    #                              'test',
    #                              CHINA, 'CSI300', {'data': data})
    db = 'test'
    collection = 'alphatest'
    manager = AlphaManager(connect)
    # manager.add_alpha(db, collection, alpha_storage)
    query = {'name': 'alpha_1'}
    alphaStorage_list = manager.query_alpha(db, collection, query)
    print(alphaStorage_list)



    # 返回是一个list list中每个对象是dict
