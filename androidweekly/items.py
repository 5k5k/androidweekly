# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AndroidWeeklyItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    img = scrapy.Field()
    id = scrapy.Field()


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    weekly_id = scrapy.Field()
    introduction = scrapy.Field()
