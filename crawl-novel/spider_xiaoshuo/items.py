import scrapy

class XiaoshuoSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()   #小说名字
    chapter_name = scrapy.Field()   #小说章节名字
    chapter_content = scrapy.Field()    #小说章节内容
