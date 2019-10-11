# -*- coding: utf-8 -*-

import re
import scrapy
from urllib.request import urlopen
from pymongo import MongoClient

mongo=MongoClient()
db=mongo["jinyong"]["xiaoshuo"]

re_paragraph = re.compile('(?<=<p>).*?(?=</p>)')

class XiaoshuoSpider(scrapy.Spider):
    name = 'xiaoshuo_spider'
    allowed_domains = ['jinyongwang.com']
    start_urls = [
        'http://www.jinyongwang.com/fei/',
        'http://www.jinyongwang.com/xue/',
        'http://www.jinyongwang.com/lian/',
        'http://www.jinyongwang.com/tian/',
        'http://www.jinyongwang.com/she/',
        'http://www.jinyongwang.com/bai/',
        'http://www.jinyongwang.com/lu/',
        'http://www.jinyongwang.com/xiao/',
        'http://www.jinyongwang.com/shu/',
        'http://www.jinyongwang.com/shen/',
        'http://www.jinyongwang.com/xia/',
        'http://www.jinyongwang.com/yi/',
        'http://www.jinyongwang.com/bi/',
        'http://www.jinyongwang.com/yuan/',
        'http://www.jinyongwang.com/yue/',
        
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