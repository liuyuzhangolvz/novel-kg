# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg

from pymongo import MongoClient

# 定义 mongodb 连接对象
mongo = MongoClient()
# 使用的 mongodb 指定数据库数据表
db = mongo['yz']['xiaoshuo']

''' 结果保存地址

保存格式

word \t tag
'''
save_path = "word_tag.txt"

print("processing...")
pairs = []
for book_obj in db.find():
    for chapter in book_obj["chapters"]:
        for word, tag in pseg.cut(chapter['content']):
            pairs.append((word, tag))

print("save to {}...".format(save_path))
# 去重
pairs_set = set(pairs)
with open(save_path, "w") as wf:
    for word, tag in pairs_set:
        wf.writelines("{}\t{}\n".format(word, tag))