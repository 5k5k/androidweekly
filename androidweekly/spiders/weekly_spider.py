# -*- coding: utf-8 -*-
import scrapy
from androidweekly.items import AndroidWeeklyItem

host = 'http://www.androidweekly.cn/'
weekly_items = []


class WeeklySpider(scrapy.Spider):
    print 'start21 '
    name = 'weekly'
    allowed_domains = ['androidweekly.cn']
    start_urls = [
        host
    ]
    custom_settings = {
        'ITEM_PIPELINES': {'androidweekly.pipelines.DuplicatesWeeklyPipeline': 200,
                           'androidweekly.pipelines.AndroidweeklyPipeline': 300},
    }

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
