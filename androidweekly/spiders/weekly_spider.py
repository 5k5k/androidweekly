# -*- coding: utf-8 -*-
import scrapy
from androidweekly.items import AndroidWeeklyItem
# from scrapy import cmdline
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from androidweekly.spiders.article_spider import ArticleSpider

# from billiard import Process

host = 'http://www.androidweekly.cn/'

weekly_items = []


# class ArticleSpider(scrapy.Spider):
#     print 'start11 '
#     name = 'article'
#     allowed_domains = ['androidweekly.cn']
#
#     start_urls = [
#     ]
#
#     for item in weekly_items:
#         start_urls.append(item['url'])
#
#     print len(start_urls)
#
#     def parse(self, response):
#         print 'start12 '
#
#         pass


class WeeklySpider(scrapy.Spider):
    print 'start21 '
    name = 'weekly'
    allowed_domains = ['androidweekly.cn']

    start_urls = [
        host
    ]

    custom_settings = {
    'ITEM_PIPELINES':{'androidweekly.pipelines.AndroidweeklyPipeline': 300},
    }
    # @staticmethod
    # def yield_page_item(author, url, title):
    #     weekly_item = AndroidWeeklyItem()
    #     print 'asfff'
    #     if author:
    #         weekly_item['author'] = author
    #     if url:
    #         weekly_item['url'] = url
    #         if title:
    #             weekly_item['title'] = title
    #
    #     yield weekly_item

    # @staticmethod
    # def close(spider, reason):
    #     # cmdline.execute("scrapy crawl article".split())
    #     # process.crawl(ArticleSpider)
    #     # process.start()
    #     return super(WeeklySpider, spider).close(spider, reason)

    # 因为有特刊所以不按照数字来去url
    def parse(self, response):
        # 获取所有url地址
        for item in scrapy.Selector(response).xpath('//article[contains(@class,"card post-wrap post")]'):
            # 图片
            img = ''
            img_style = item.xpath('div[contains(@class,"card-header")]/a/div/@style').extract()
            if img_style:
                if img_style[0].__contains__('background-image'):
                    img = img_style[0].encode('utf-8').split("background-image:")[1].split('url(')[1].split(')')[0]
                    if img.startswith('/'):
                        img = host + img
                    print img

            # 作者
            author = item.xpath(
                'div[contains(@class,"card-header")]/div[@class="author"]/a/span/text()').extract()[0].encode('utf-8')
            print author

            a = item.xpath('div[@class="content"]/h2/a')
            # url
            url = a.xpath('@href').extract()[0].encode('utf-8')
            print url

            # 标题
            title = a.xpath('text()').extract()[0].encode('utf-8')
            print title

            weekly_item = AndroidWeeklyItem()
            if author:
                weekly_item['author'] = author
            if url:
                weekly_item['url'] = url
            if title:
                weekly_item['title'] = title
            weekly_item['img'] = img
            weekly_items.append(weekly_item)
            yield weekly_item

        # 载入下一页
        next_page = scrapy.Selector(response).xpath('//a[@class="older-posts ripple"]/@href').extract()
        if next_page:
            yield scrapy.http.Request(host + next_page[0], callback=self.parse)
        # else:
        #     settings = get_project_settings()
        #     process = CrawlerProcess(settings)
        #     process.crawl(ArticleSpider())
        #     process.start()
        # else:
        #     cmdline.execute("scrapy crawl article".split())


# class CrawlerScript(Process):
#     def __init__(self, spider, job):
#         Process.__init__(self)
#         self.crawler = CrawlerRunner()
#         self.crawler.crawl(spider, job=job)


# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })

# process = CrawlerProcess()
# process.crawl(WeeklySpider)
# process.crawl(ArticleSpider)
# process.start()

# configure_logging()
# runner = CrawlerRunner()


# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(WeeklySpider)
#
#     yield runner.crawl(ArticleSpider)
#     reactor.stop()
#
# crawl()
# reactor.run()
