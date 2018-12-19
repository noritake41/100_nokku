# coding: utf-8
import json
import pymongo
from pymongo import MongoClient

client = MongoClient()
db = client.testdb
collection = db.artist

results = collection.find({'tags.value': 'dance'})

results.sort('rating.count', pymongo.DESCENDING)

for i, doc in enumerate(results[0:10], start=1):
    if 'rating' in doc:
        rating = doc['rating']['count']
    else:
        rating = '(none)'
    print('{}(id:{})\t{}'.format(doc['name'], doc['id'], rating))
