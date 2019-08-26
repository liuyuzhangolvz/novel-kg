# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# -*- coding: utf-8 -*-
import os
 
class SpiderXiaoshuoPipeline(object):
 
    def process_item(self, item, spider):
        curPath = 'F:\金庸全套小说'
        tempPath = str(item['name'])
        targetPath = curPath + os.path.sep + tempPath
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)
 
        filename_path = 'F:\金庸全套小说'+ os.path.sep + str(item['name'])+ os.path.sep + str(item['chapter_name']) + '.txt'
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(item['chapter_content'] + "\n")
        return item
