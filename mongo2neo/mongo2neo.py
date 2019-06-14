# -*-  coding: utf-8 -*-

from pymongo import MongoClient
from py2neo import Node, Relationship, Graph, NodeMatcher

mongo = MongoClient()
db = mongo['yz']['persons']

#graph = Graph('127.0.0.1:7474', user='neo4j',password='123456')
graph = Graph()
matcher = NodeMatcher(graph)
graph.delete_all()

def look_and_create(name):
    end = matcher.match("Jinyong", name=name).first()
    if end is None:
        end = Node('Jinyong', name=name)           
    return end

def insert_one_data(arr):
    start = look_and_create(arr[0])
    items = [arr[2]] if isinstance(arr[2], str) else arr[2]
    for name in items:
        end = look_and_create(name)
        r = Relationship(start, arr[1], end, name=arr[1])   
        graph.create(r)

def insert_datas():
    print('transfering...')
    for data in db.find():
        print(data)
        for key, val in data['info'].items():
            if not key.strip() or not val:
                continue
            insert_one_data([data['person'], key, val])

if __name__ == "__main__":
    insert_datas()
