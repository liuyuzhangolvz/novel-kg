# novel-kg
金庸小说人物关系图谱构建

---

# 环境

```
Python 3.6+
MongoDB
Neo4j
```

⚠️ 请先启动 MongoDB 和 Neo4j 

# 目录结构
```
|- 
  |- crawl-baike  爬取百度百科
  |- crawl-novel  爬取小说
  |- kgqa  知识图谱文档
  |- mongo2neo  mongo 数据导入 neo4j
```

# 操作说明

**1.爬取金庸小说数据**

启动 MongoDB 进程，执行爬虫文件 xiaoshuo_spider.py ，得到小说文本存入MongoDB。
```
cd crawl-baike
scrapy crawl spider_xiaoshuo
```
**2.爬取小说人物关系**

- 执行转换脚本  convert.py，将 MongoDB 中的小说数据转成文本存到本地。
```
cd crawl-novel
python convert.py
```

- 执行 extract_persons.py ，对小说文本进行词法分析，提取出人名
```
python extract_persons.py
```

- 执行爬虫，根据人名爬取百度百科相关的属下和关系，存入MongoDB。
```
scrapy crawl person_spider
```
**3.MongoDB 转 Neo4j**

执行转换脚本 mongo2neo.py，将 MongoDB 中数据导入 Neo4j 。
```
cd mongo2neo
python mongo2neo.py
```


# 效果
## 人物关系知识图谱
全部人物关系图
![persons relations](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/graph.png)

“张无忌”的人物关系图
![张无忌](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/%E5%BC%A0%E6%97%A0%E5%BF%8C.png)

# 图谱问答系统
```
cd kgqa
python app.py
```

系统架构
![wenda index](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/kgqa.png)

关于张无忌的问答
![wenda zhangwuji](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/wenda-zhangwuji.png)

关于周芷若的问答
![wenda zhouzhiruo](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/wenda-zhouzhiruo.png)
