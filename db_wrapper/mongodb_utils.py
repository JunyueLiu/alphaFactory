from pymongo import MongoClient, database, CursorType
from pymongo.results import UpdateResult
import pandas as pd
import os
from data_downloader.multi_asset_data_merger import merge_single_asset



class MongoConnection:

    def __init__(self, host, port, user, password):
        self.client = MongoClient(host, port, username=user, password=password)

    def read_mongo_df(self, db: str, collection: str, query=None, projection=None, no_id=True):
        """ Read from Mongo and Store into DataFrame """
        # The `projection` argument is used to specify a subset
        # of fields that should be included in the result documents.
        cursor = self.client[db][collection].find(query, projection, cursor_type=CursorType.EXHAUST)

        df = pd.DataFrame.from_records(cursor)
        #df = pd.DataFrame(list(cursor))  # todo This is problematic because of efficiency.
        # todo See https://stackoverflow.com/questions/16249736/how-to-import-data-from-mongodb-to-pandas
        # Delete the _id
        if no_id:
            try:
                del df['_id']
            except:
                pass

        return df



    def insert_from_dataframe(self, db: str, collection_name: str, df: pd.DataFrame) -> UpdateResult:
        records = df.to_dict('records')

        result = self.client[db][collection_name].insert_many(records)
        return result

    def insert_from_dict(self, db: str, collection_name: str, data:dict):
        result = self.client[db][collection_name].insert_one(data)
        return result

    def get_ohlc_dataframe(self, db, collection, query=None, no_id=True, field_name_set=None) -> pd.DataFrame:
        if field_name_set is None:
            field_name_set = {'time_key', 'close', 'open', 'high', 'low', '_id'}
        return self.read_mongo_df(db, collection, query, field_name_set, no_id)

    def build_ohlc_document(self, db: str, collection_name: str, df: pd.DataFrame, time_key='time_key') -> None:
        if collection_name in self.client.get_database(db).list_collection_names():
            raise ValueError('{} exists in {}.'.format(collection_name, db))
        records = df.to_dict('records')
        self.client[db][collection_name].insert_many(records)
        self.client[db][collection_name].create_index(time_key, unique=True)

