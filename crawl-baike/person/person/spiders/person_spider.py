# -*- coding: utf-8 -*-

""" 爬取人物百度百科 infobox
"""

import re
import scrapy
from pymongo import MongoClient

# 常量
PERSONS_FILE = 'D:/毕业设计/crawl/persons.txt' # 人物列表存放地址，这里最好用绝对地址哦
# 变量
mongo = MongoClient()  # mongodb 的操作对象，使用默认参数即可
db = mongo["yz"]["persons"]  # yz 是 mongo 的数据库， persons 是库 yz 下的一张表
re_split = re.compile(r'[,、，；]')  # 字符串切割正则

def strQ2B(content):
    """全角转半角"""
    content = str(content)
    rstring = ""
    for uchar in content:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += chr(inside_code)
    return rstring

def clean_content(content):
    """
    文本清洗:
    - 去除 html 标签、实体
    - 去除 url
    - 去除 \t \n 等符号
    """

    content = strQ2B(content)
    re_del = re.compile(r'<[^>]+>|\s+|\&\w+\;|http://[a-zA-Z0-9.?/&=:]*',re.S)
    content = re_del.sub("", content)
    content = content.replace(" ","")
    return content


def get_urls():
    """从人物列表中获取url"""
    url_format = 'https://baike.baidu.com/item/{}'
    urls = []
    with open(PERSONS_FILE, 'r', encoding="utf-8") as rf:
        for line in rf:
            urls.append(url_format.format(line.strip()))
    return urls

class PersonSpider(scrapy.Spider):
    """主爬虫类，需要继承 scrapy 的 Spider 类"""
    name = 'person_spider' # 爬虫名称，和文件名一致
    allowed_domins = ['baike.baidu.com'] # 允许爬取的域名
    start_urls = get_urls() # 要爬去的 url
    fail_handle = open('./fail.txt', 'w') # 失败的文件资源，对于插入失败的人物可能是百科中出现了歧义，所以需要人工检查插入

    def parse(self, response):
        """ 解析页面，这里只存储 basic-info 的内容，且要判断 '金庸' 二字是否出现在页面中
        """
        # 通过 xpath 语法获取当前人物名
        person = response.xpath("//dd[@class='lemmaWgt-lemmaTitle-title']//h1/text()").extract_first()
        if '金庸' in clean_content(response.xpath("//div[@class='content-wrapper']").extract_first()):
            # names 代表 basic-info 里的键名
            names = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'basic-info')]//dt[contains(concat(' ', normalize-space(@class), ' '), 'name')]").extract()
            # vals 代表 baisic-info 里的值
            vals = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'basic-info')]//dd[contains(concat(' ', normalize-space(@class), ' '), 'value')]").extract()
            # 这里使用断言判断 names 的个数和 vals 的能对齐
            assert len(names) == len(vals)
            # 对 names 和 vals 进行规范化
            names = [clean_content(x) for x in names]
            values = []
            for val in vals:
                val = clean_content(val)
                arr = [str(x) + ')' for x in val.split(")")] if val.count(')') > 1 else re_split.split(val)
                if len(arr) > 1:
                    values.append(arr)
                else:
                    values.append(arr[0])

            if not values:
                # 失败则插入文件
                self.fail_handle.writelines("{} {}\n".format(str(person), response._url))
            else:
                # 插入 mongodb
                info = dict(zip(names, values))
                del info["中文名"]
                db.save({"person": person, "info": info})#zip把names，values两个列表转换成键值对
        else:
            if person is not None:
                # 失败则插入文件
                self.fail_handle.writelines("{} {}\n".format(str(person), response._url))