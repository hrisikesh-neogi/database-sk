#for mongodb
import os
import pandas as pd
import pymongo
import json
import logging as lg

lg.basicConfig(filename='sending_Class.log', level=lg.INFO, format='%(asctime)s %(message)s')

class mongo_operation:
    def __init__(self, client_url, db):
        self.client_url = client_url
        self.db = db


    def insert_oneData(self, collection_name, record):
        """
        insert one record to mongodb
        :param collection_name: name of the collection
        :param record: the data
        : insert no: the number of record to insert
        """
        client = pymongo.MongoClient(self.client_url)
        db = client[self.db]

        collection = db[str(collection_name)]
        collection.insert_one(record)
        print(f'one record has been inserted. \n record :{record}')
        lg.info(f'one record has been inserted. \n record was :{record}')

    def bulk_insert(self, path, collection_name):
        """ insert data from csv file to mongodb
        takes :
        param : path : path of the csv file
        param : collection_name : name of the collection
        
        """

        mng_client = pymongo.MongoClient(self.client_url)
        mng_db = mng_client[self.db]
        self.db_collection = mng_db[collection_name]

        data = pd.read_csv(path)
        data_json = json.loads(data.to_json(orient='records'))
        self.db_collection.insert(data_json)
        print('data inserted ')
        lg.info('data inserted successfully')


    def find(self, collection_name, query):
        """
        method find : to find data in mongo database
        returns dataframe of the searched data. 
        takes :
        param : collection_name : name of the collection,
        param : query : query to find the data in mongo database -- example of query "{"name":"sourav"}"
        """
        mng_client = pymongo.MongoClient(self.client_url)
        mng_db = mng_client[self.db]
        self.db_collection = mng_db[collection_name]
        cursor = self.db_collection.find(query)
        print(cursor)
        lg.info(cursor)
        data =  pd.DataFrame(list(cursor))
    

        return data 
    