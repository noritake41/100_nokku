# coding: utf-8
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

def support_ObjectId(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")

client = MongoClient()
db = client.testdb
collection = db.artist

for i, doc in enumerate(collection.find({'name': 'Queen'}), start=1):
    print('{}件目の内容:\n{}'.format(i, json.dumps(doc, indent='\t', ensure_ascii=False, sort_keys=True, default=support_ObjectId)))
