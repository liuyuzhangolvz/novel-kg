# novel-kg [WIP]
金庸小说人物关系图谱构建

---

# Environment

```
Python 3.6+
MongoDB
Neo4j
```

# 操作说明

**1.爬取金庸小说数据**

启动 MongoDB 进程，执行爬虫文件 xiaoshuo_spider.py ，得到小说文本存入MongoDB。
```
scrapy crawl spider_xiaoshuo
```
执行转换脚本  convert.py，将 MongoDB 中的小说数据转成文本存到本地。
```
python convert.py
```
**2.获取小说中的人名**

执行 extract_persons.py ，对小说文本进行词法分析，提取出人名
```
python extract_persons.py
```
**3.通过人名爬取百度百科**

执行爬虫文件 person_spider.py，根据人名爬取百度百科相关的属下和关系，存入MongoDB。
```
scrapy crawl person_spider
```
**4.MongoDB 转 Neo4j**

执行转换脚本 mongo2neo.py，将 MongoDB 中数据导入 Neo4j 。
```
python mongo2neo.py
```

# Results
启动 neo4j：`neo4j.bat console`
## 人物关系知识图谱
全部人物关系图
![persons relations](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/graph.png)

“张无忌”的人物关系图
![张无忌](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/%E5%BC%A0%E6%97%A0%E5%BF%8C.png)

## 基于 d3.js 的图谱问答系统
```
python app.py
```
系统架构
![wenda index](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/kgqa.png)

关于张无忌的问答
![wenda zhangwuji](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/wenda-zhangwuji.png)

关于周芷若的问答
![wenda zhouzhiruo](https://github.com/liuyuzhangolvz/novel-kg/blob/master/docs/wenda-zhouzhiruo.png)
