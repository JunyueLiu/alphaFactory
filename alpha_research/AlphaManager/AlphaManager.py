from db_wrapper.mongodb_utils import MongoConnection
from alpha_research.factor_zoo.alpha_101 import *
from alpha_research.SingleAssetResearch import *
import pandas as pd
import pickle
import inspect
import datetime
import traceback

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from alpha_research.AlphaManager.app import app
import base64
import datetime
import io
import dash_table


# from db_wrapper.mongodb_utils import *

HK = 'HK'
CHINA = 'CN'
US = 'US'
EUROPE = 'EU'
JAPAN = 'JP'



class AlphaStorage:
    def __init__(self, name: str, author: str,
                 alpha_function,
                 alpha_parameter: dict,
                 alpha_idea: str,
                 alpha_regions: str or list,# can be defined using the liquidity profile, such as TOP50, TOP100, TOP200, TOP1500
                 alpha_universe: str or list,  # index
                 performance_parameter: dict):
        self.name = name
        self.author = author
        self.include_time = datetime.datetime.now()
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
            df = dic['performance_parameter']['data']
            save_dict = {}
            if isinstance(df.index, pd.MultiIndex):
                save_dict['code'] = df.index.get_level_values(1).unique().to_list()
                time = df.index.get_level_values(0).unique().sort_values()

                save_dict['start'] = time[0]
                save_dict['end'] = time[-1]
            elif isinstance(df.index, pd.Index):
                if 'code' in df.columns:
                    save_dict['code'] = df['code'][0]
                time = df.index.unique().sort_values()
                save_dict['star'] = time[0]
                save_dict['end'] = time[-1]
            dic['performance_parameter']['data'] = save_dict
        elif isinstance(dic['performance_parameter']['data'], dict):
            pass

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
        alphaStorage = AlphaStorage(input_dict['name'], input_dict['author'],
                                    input_dict['alpha_function'],
                                    input_dict['alpha_parameter'],
                                    input_dict['alpha_idea'],
                                    input_dict['alpha_regions'],
                                    input_dict['alpha_universe'],
                                    input_dict['performance_parameter'])
        return alphaStorage

    def query_alpha_by_datasets(self, db, collection,
                                datasets: dict or pd.DataFrame):

        search_dict = {}
        if isinstance(datasets, pd.DataFrame):
            if isinstance(datasets.index, pd.MultiIndex):
                search_dict['code'] = datasets.index.get_level_values(1).unique().to_list()
                time = datasets.index.get_level_values(0).unique().sort_values()

                search_dict['start'] = time[0]
                search_dict['end'] = time[-1]
            elif isinstance(datasets.index, pd.Index):
                if 'code' in datasets.columns:
                    search_dict['code'] = datasets['code'][0]
                time = datasets.index.unique().sort_values()
                search_dict['star'] = time[0]
                search_dict['end'] = time[-1]
        elif isinstance(datasets, dict):
            search_dict = dict

        alpha_storage_list = self.query_alpha(db, collection, {'performance_parameter': {'data': search_dict}})
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


class AlphaManagerPage:

    def connect_server(self,ip, port, username, password):
        self.connect = MongoConnection(ip, port, username, password)
        self.manager = AlphaManager(self.connect)
        return self.connect.client.list_database_names()
        # db = 'test'
        # collection = 'alphatest'
        # ll = manager.query_alpha_by_alpha_idea(db, collection, 'test')
        # return ll

    def dash_webpage(self):
        """
        :return:
        """

        app.layout = html.Div(children=[
            html.H1('Alpha manager'),
            html.Div(['IP  ', dcc.Input(id='ip_address', value='120.55.45.12', type='text'),
                      'Port  ', dcc.Input(id='port_number', value='27017', type='number')]),
            html.Div(['User  ', dcc.Input(id='username', value='root', type='text'),
                      'Possword  ', dcc.Input(id='password', value='AlphaFactory2020', type='password')]),
            html.Button(id='connect-button', n_clicks=0, children='Connect server'),
            html.Div(id='connect-result'),
            html.Hr(),
            html.Div(['Database:  ', dcc.Input(id='database', value='test', type='text'),'  ',
                      html.Button(id='connect_database_button', n_clicks=0, children='Connect database')]),
            html.Div(id='table-name'),
            html.Div(['Table:  ', dcc.Input(id='table', value='alphatest', type='text')]),
            html.Hr(),
            html.Div(['Alpha idea:  ', dcc.Input(id='alpha_idea', value='test', type='text'),'  ',
                      html.Button(id='query_by_idea_button', n_clicks=0, children='Query by idea')]),
            html.Div(id='query-result'),
            html.Div(['Alpha name:  ', dcc.Input(id='alpha_name', value='alpha_6', type='text'), '  ',
                      html.Button(id='query_by_name_button', n_clicks=0, children='Query by name')]),



            html.Div(id='query-result2'),
            # upload box
            dcc.Upload(id='upload-data',
                children=html.Div([
                    'Query by ',
                    html.A('Datasets')
                ]),       style={
            'width': '300px',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'}),
            html.Div(id='query-result3'),
            html.Div(id='output-data-upload'),


        ], style={'margin': '20px'})



        @app.callback(Output('connect-result', 'children'),
                      [Input('connect-button', 'n_clicks')],
                      [State('ip_address', 'value'),
                       State('port_number', 'value'),
                       State('username', 'value'),
                       State('password', 'value'),
                       ])
        def connect_server(n_clicks, ip, port, username, password):
            if n_clicks != 0:
                namelist = self.connect_server(ip, int(port), username, password)
                return str(namelist)


        @app.callback(Output('table-name', 'children'),
                      [Input('connect_database_button', 'n_clicks')],
                      [State('database', 'value')])
        def connect_db(n_clicks, database):
            if n_clicks != 0:
                tablelist = self.connect.client[database].list_collection_names()
                return str(tablelist)

        @app.callback(Output('query-result', 'children'),
                      [Input('query_by_idea_button', 'n_clicks')],
                      [State('database', 'value'),
                       State('table', 'value'),
                       State('alpha_idea', 'value')
                       ])
        def query_by_idea(n_clicks, db,collection,alpha_idea):
            if n_clicks != 0:
                result = self.manager.query_alpha_by_alpha_idea(db, collection, alpha_idea)
                return str(result)

        @app.callback(Output('query-result2', 'children'),
                      [Input('query_by_name_button', 'n_clicks')],
                      [State('database', 'value'),
                       State('table', 'value'),
                       State('alpha_name', 'value')
                       ])
        def query_by_name(n_clicks, db, collection, alpha_name):
            if (n_clicks != 0):
                result = self.manager.query_alpha_by_alpha_name(db, collection, alpha_name)
                return str(result)

        # read scv file
        def parse_contents(contents, filename, date):
            content_type, content_string = contents.split(',')

            decoded = base64.b64decode(content_string)
            try:
                if 'csv' in filename:
                    # Assume that the user uploaded a CSV file
                    df = pd.read_csv(
                        io.StringIO(decoded.decode('utf-8')))
                    df['time_key'] = pd.to_datetime(df['time_key'])
                    df.set_index('time_key', inplace=True)
                    self.data = df[-1000:]
                elif 'xls' in filename:
                    # Assume that the user uploaded an excel file
                    df = pd.read_excel(io.BytesIO(decoded))
            except Exception as e:
                print(e)
                return html.Div([
                    'There was an error processing this file.'
                ])

            return html.Div([
                html.H5(filename),
                html.H6(datetime.datetime.fromtimestamp(date)),

                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                )
            ])

        @app.callback(Output('query-result3', 'children')
                       # ,Output('output-data-upload', 'children')
                       ,
                      [Input('upload-data', 'contents')],
                      [State('database', 'value'),
                       State('table', 'value'),
                       State('upload-data', 'filename'),
                       State('upload-data', 'last_modified')])

        def update_output(list_of_contents, db, collection, list_of_names, list_of_dates):
            if list_of_contents is not None:

                parse_contents(list_of_contents, list_of_names, list_of_dates)

                result = self.manager.query_alpha_by_datasets(db, collection, self.data)
                return str(result)


        return app

# 查的时候可以查出alpha有多少
# todo:测试alpha
if __name__ == '__main__':

    # sample data
    # data_path = r'../HK.999010_2019-06-01 00:00:00_2020-05-30 03:00:00_K_1M_qfq.csv'
    # df = pd.read_csv(data_path)
    # df['time_key'] = pd.to_datetime(df['time_key'])
    # df.set_index('time_key', inplace=True)
    # data = df[-1000:]

    # connect mongodb
    AlphaManagerPage().dash_webpage().run_server(debug=True)

    ll = manager.query_alpha_by_alpha_idea(db, collection, 'test')
    print(ll)
    ll = manager.query_alpha_by_alpha_name(db, collection, 'alpha_6')
    print(ll)
    ll = manager.query_alpha_by_datasets(db, collection, data)
    print(ll)



