import pymongo
import datetime

mongo_client = pymongo.MongoClient('127.0.0.1', 27017)

print(mongo_client.server_info())

mongo_db = mongo_client['db91']
mongo_collection = mongo_db['video']

find_result_cursor = mongo_collection.find()

for find_result in find_result_cursor:
    print(find_result)