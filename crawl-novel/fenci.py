# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg

from pymongo import MongoClient

# 定义 mongodb 连接对象
mongo = MongoClient()
# 使用的 mongodb 指定数据库数据表
db = mongo['jinyong']['xiaoshuo']
save_path = "F:/jinyong/data/persons.txt"

print("start processing...")
persons = []
for book_obj in db.find():
    for chapter in book_obj["chapters"]:
        for word, tag in pseg.cut(chapter['content']):
            if tag == "nr":
              persons.append(word)
print("save to {}...".format(save_path))
# 去重
persons = list(set(persons))
with open(save_path, "w") as wf:
    for word in persons:
        wf.writelines("{}\n".format(word))