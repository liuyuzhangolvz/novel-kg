# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import jieba
import jieba.posseg as pseg
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

# mongodb 操作对象
mongo = MongoClient()
db = mongo["jinyong"]["persons"]

# flask 实例对象
app = Flask(__name__)

# 将 mongodb 存放的数据格式转成 d3.js 的三元组格式

"""
d3.js 的具体数据格式示例：

[
  nodes: {
      "name": "张无忌",  // 0
      "name": "赵敏",    // 1
      "name": "明教"     // 2
  },
  edges: {
     "source": 0, "target": 1, "label": "女友", "type": "info",  // 从 0 到 1 的关系名称(label)是女友，边的类型是 info
     "source": 0, "target": 2, "label": "门派", "type": "answer" // 从 0 到 1 的关系名称是门派，边的类型是 answer
  }
]

其中 type 代表边的类型，如果类型是 answer 则说明这条边上的关系是当前查询的答案，所以前端显示时会变绿色
""" 
def get_links(data, query):
    answers = []
    nodes, edges = [{"name": data["person"]}], []
    for idx, (key, val) in enumerate(data["info"].items(), 1):
        nodes.append({"name": val})
        edge = {"source": 0, "target": idx, "label": key, "type": "info"}
        if key in query:
            answers.append((key, val))
            edge["type"] = "answer"
        edges.append(edge)
    return {"nodes": nodes, "edges": edges}, answers


# 定位到系统的首页
@app.route('/')
def index():
    return render_template('index.html')


# 处理查询请求
@app.route("/search", methods=["POST", "GET"])
def get_search():
    query = request.form.get("query")
    person = None
    for word, flag in pseg.cut(query):
        if flag == "nr":
            person = word
            break
    if person is not None:
        for ret in db.find({"person": person}):
            links, answers = get_links(ret, query)
            return jsonify({"code": 200, "links": links, "answers": answers})
    return jsonify({"code": 100, "data": {}})


# 系统入口函数
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
