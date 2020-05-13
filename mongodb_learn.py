import pymongo
import datetime

mongo_client = pymongo.MongoClient('127.0.0.1', 27017)

print(mongo_client.server_info())

mongo_db = mongo_client['dbtest']
mongo_collection = mongo_db['video']
mongo_collection.drop()

videolist = [{'id': 1, 'title': 'video1', 'num': 1},
             {'id': 2, 'title': 'video2', 'num': 2},
             {'id': 3, 'title': 'video3', 'num': 3},
             {'id': 4, 'title': 'video4', 'num': 4},
             {'id': 5, 'title': 'video5', 'num': 5},
             {'id': 6, 'title': 'video6', 'num': 6}]

mongo_collection.insert_many(videolist)

find_result_cursor = mongo_collection.find()

for find_result in find_result_cursor:
    print(find_result)

print('===================================================')

videolist2 = [{'id': 1, 'title': 'video1', 'num': 1},
              {'id': 2, 'title': 'video2', 'num': 2},
              {'id': 3, 'title': 'video3', 'num': 6},
              {'id': 4, 'title': 'video4', 'num': 4},
              {'id': 8, 'title': 'video8', 'num': 8},
              {'id': 5, 'title': 'video5', 'num': 5},
              {'id': 6, 'title': 'video6', 'num': 12}]

for video in videolist2:
    find_result = mongo_collection.find_one({'id': video['id']})
    if find_result == None:
        # 下载
        mongo_collection.insert_one(video)
    elif video['num'] > find_result['num']:
        mongo_collection.update_one({'id': video['id']}, {'$set': video})

# mongo_collection.insert_many(videolist2)

find_result_cursor = mongo_collection.find().sort([('num', -1)])

for find_result in find_result_cursor:
    print(find_result)

today = datetime.date.today()
print(today)
