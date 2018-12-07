# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class DataApiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content = scrapy.Field()
    readView = scrapy.Field()
    dt = scrapy.Field()
    commentCount = scrapy.Field()
    postUrl = scrapy.Field()
    shareCount = scrapy.Field()
    likeCount = scrapy.Field()
    userLink = scrapy.Field()
    fansCount = scrapy.Field()
    postName = scrapy.Field()
    search_word = scrapy.Field()
    spider_date = scrapy.Field()
    table_name = scrapy.Field()

class BaiduDataApiItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    parentAppCode = scrapy.Field()
    search_word = scrapy.Field()
    spider_date = scrapy.Field()
    table_name = scrapy.Field()

class ToutiaoDataApiItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    publisher = scrapy.Field()
    search_word = scrapy.Field()
    spider_date = scrapy.Field()
    table_name = scrapy.Field()


class ToutiaoDateDataApiItem(scrapy.Item):
    title = scrapy.Field()
    publish_date = scrapy.Field()
    spider_date = scrapy.Field()
    table_name = scrapy.Field()

class ZhihuQuestionDetailItem(scrapy.Item):
    qid = scrapy.Field()
    followed = scrapy.Field()
    viewed = scrapy.Field()
    topic_id = scrapy.Field()
    aid_num = scrapy.Field()
    spider_date = scrapy.Field()
    table_name = scrapy.Field()
