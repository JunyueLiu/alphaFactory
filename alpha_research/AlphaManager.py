from db_wrapper.mongodb_utils import MongoConnection

HK = 'HK'
CHINA = 'CN'
US = 'US'
EUROPE = 'EU'
JAPAN = 'JP'


class AlphaStorage:
    def __init__(self, name: str,
                 alpha_function,
                 alpha_parameter: dict,
                 alpha_idea: str,
                 alpha_regions: str or list,
                 alpha_universe: str or list,
                 performance_parameter: dict):
        self.name = name
        self.alpha_function = alpha_function
        self.alpha_parameter = alpha_parameter
        # alpha_parameter {'select_parameter':{'para1': var1, 'para2': var1, ...},
        #                   'parameter_range': {'para1': {'type': int, 'range':[]},
        #                   'para2': {'type': float, 'range':[]}
        #                   , ...},}
        self.alpha_idea = alpha_idea
        self.alpha_regions = alpha_regions
        self.alpha_universe = alpha_universe
        self.performance_parameter = performance_parameter
        # performance_parameter
        # {'data': 'selection query or somehow identify the data from the dataset'
        # 'performance':{
        #
        #
        # }}

    def to_dict(self):
        return vars(self)


class AlphaManager:
    def __init__(self, mongo_con: MongoConnection):
        self.mongo_conn = mongo_con
        pass

    def add_alpha(self):
        pass

    def query_alpha(self):
        pass

    def query_alpha_by_name(self):
        pass

    def query_alpha_by_regions(self, regions: str):
        pass

    def query_alpha_by_datasets(self, datasets: str):
        pass

    def alpha_vs_alpha(self):
        pass


if __name__ == '__main__':
    alpha_storage = AlphaStorage('test', print, {'selected': {'para1': 1},
                                                 'parameter_range': {'para1': {'type': int, 'range': [1, 2]}}}, 'test',
                                 CHINA, 'CSI300', {})

