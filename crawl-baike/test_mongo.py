# -*- coding:utf-8 -*-

from pymongo import MongoClient

mongo = MongoClient()

db = mongo["yz"]["persons"]

if db.save({"name": "xm"}):
	print("yes")
else:
	print("no")

for item in db.find():
	print(item)