# -*- coding: utf-8 -*-
import scrapy
import re
from urllib.request import urlopen
from pymongo import MongoClient

mongo=MongoClient()
db=mongo["yz"]["xiaoshuo"]

re_paragraph = re.compile('(?<=<p>).*?(?=</p>)')

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo_spider'
    allowed_domains = ['jinyongwang.com']
    start_urls = [
        'http://www.jinyongwang.com/fei/',#飞狐外传
        'http://www.jinyongwang.com/xue/',#雪山飞狐
        'http://www.jinyongwang.com/lian/',#连城诀
        'http://www.jinyongwang.com/tian/',#天龙八部
        'http://www.jinyongwang.com/she/',#射雕英雄传
        'http://www.jinyongwang.com/bai/',#白马啸西风
        'http://www.jinyongwang.com/lu/',#鹿鼎记
        'http://www.jinyongwang.com/xiao/',#笑傲江湖
        'http://www.jinyongwang.com/shu/',#书剑恩仇录
        'http://www.jinyongwang.com/shen/',#神雕侠侣
        'http://www.jinyongwang.com/xia/',#侠客行
        'http://www.jinyongwang.com/yi/',#倚天屠龙记
        'http://www.jinyongwang.com/bi/',#碧血剑
        'http://www.jinyongwang.com/yuan/',#鸳鸯刀
        'http://www.jinyongwang.com/yue/',#越女剑
    ] #金庸王全套小说
 
    #获取小说章节的URL
    def parse(self, response):

        cnt_url = "/".join(response._url.strip("/").split("/")[:-1])
        name = response.xpath('//div[@class="pu_breadcrumb"]//h3[@class="set"]/font/text()').extract_first()
        chapter_names = response.xpath('//ul[@class="mlist"]//li/a/text()').extract()
        chapter_urls = response.xpath('//ul[@class="mlist"]//li/a/@href').extract()
        
        chapters = []
        for chapter_name, chapter_url in zip(chapter_names, chapter_urls):
            chapter_name = chapter_name.replace("\u3000", " ")
            response = urlopen(cnt_url + chapter_url)
            html = response.read().decode("utf-8")
            texts = re_paragraph.findall(str(html))
            chapters.append({"name": chapter_name, "content": "\n".join(texts)})
        
        db.save({"book_name": name, "chapters": chapters})
