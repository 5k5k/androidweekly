# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import codecs
# import json
import pymysql
from scrapy.exceptions import DropItem
import redis


def db_handler():
    conn = pymysql.connect(
        host="localhost",
        user='root',
        passwd='root123456',
        charset='utf8',
        use_unicode=False
    )
    return conn


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.StrictRedis(connection_pool=pool)


# 存储周列表页信息
class AndroidweeklyPipeline(object):
    def process_item(self, item, spider):
        db = db_handler()
        cursor = db.cursor()

        sql = 'insert into androidweekly.weekly_page(title,author,img,url) VALUES (%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (item['title'], item['author'], item['img'], item['url']))
            db.commit()
            item['id'] = cursor.lastrowid
        except Exception, e:
            print e
            db.rollback()
        return item


# 存储文章信息
class ArticlePipeline(object):
    def process_item(self, item, spider):
        db = db_handler()
        cursor = db.cursor()

        sql = 'insert into androidweekly.article(title,url,page_id,category,introduction) VALUES (%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,
                           (item['title'], item['url'], item['weekly_id'], item['category'], item['introduction']))
            db.commit()
        except Exception, e:
            print e
            db.rollback()
        return item


# 用redis去重
class DuplicatesWeeklyPipeline(object):
    def process_item(self, item, spider):
        if r.exists('weekly url:%s' % item['url']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            r.set('weekly url:%s' % item['url'], 1)
        return item
