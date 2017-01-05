# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import codecs
# import json
import pymysql
from androidweekly.spiders.weekly_spider import WeeklySpider
from androidweekly.spiders.article_spider import ArticleSpider


def db_handler():
    conn = pymysql.connect(
        host="localhost",
        user='root',
        passwd='root123456',
        charset='utf8',
        use_unicode=False
    )
    return conn


class AndroidweeklyPipeline(object):
    # def __init__(self):
    #     self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line.decode('unicode_escape'))
        db = db_handler()
        cursor = db.cursor()

        # if spider == WeeklySpider:
        sql = 'insert into androidweekly.weekly_page(title,author,img,url) VALUES (%s,%s,%s,%s)'
        try:
            cursor.execute(sql, (item['title'], item['author'], item['img'], item['url']))
            db.commit()
            item['id'] = cursor.lastrowid
        except Exception, e:
            print e
            db.rollback()
        # elif spider == ArticleSpider:
        #     sql = 'insert into androidweekly.article(title,url,page_id,category,introduction) VALUES (%s,%s,%d,%s,%s)'
        #     try:
        #         cursor.execute(sql,
        #                        (item['title'], item['url'], item['weekly_id'], item['category'], item['introduction']))
        #         db.commit()
        #     except Exception, e:
        #         print e
        #         db.rollback()

        return item


class ArticlePipeline(object):
    # def __init__(self):
    #     self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        # self.file.write(line.decode('unicode_escape'))
        db = db_handler()
        cursor = db.cursor()

        # if spider == WeeklySpider:
        #     sql = 'insert into androidweekly.weekly_page(title,author,img,url) VALUES (%s,%s,%s,%s)'
        #     try:
        #         cursor.execute(sql, (item['title'], item['author'], item['img'], item['url']))
        #         db.commit()
        #         item['id'] = cursor.lastrowid
        #     except Exception, e:
        #         print e
        #         db.rollback()
        # elif spider == ArticleSpider:
        sql = 'insert into androidweekly.article(title,url,page_id,category,introduction) VALUES (%s,%s,%s,%s,%s)'
        try:
            cursor.execute(sql,
                           (item['title'], item['url'], item['weekly_id'], item['category'], item['introduction']))
            db.commit()
        except Exception, e:
            print e
            db.rollback()

        return item
