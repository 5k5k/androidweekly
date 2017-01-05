# -*- coding: utf-8 -*-
import scrapy
from androidweekly.items import ArticleItem

host = 'http://www.androidweekly.cn'


class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['androidweekly.cn']
    start_urls = []
    items = []
    custom_settings = {
        'ITEM_PIPELINES': {'androidweekly.pipelines.ArticlePipeline': 300},
    }

    def __init__(self, name=None, items=None, **kwargs):
        super(ArticleSpider, self).__init__(name, **kwargs)
        for item in items:
            print item['url']
            self.start_urls.append(host + item['url'])
        self.items = items

    def parse(self, response):
        weekly_id = None
        for item in self.items:
            if host + item['url'] == response.url:
                # 如果id没有值说明没有存入数据库
                if 'id' not in item.keys():
                    return
                weekly_id = item['id']
                break

        for category in response.xpath('//div[@class="post-entry"]/h3'):
            category_name = category.xpath('text()').extract_first().encode('utf8')
            if (category_name == '捐赠') or (category_name == '版权声明'):
                continue
            print category_name

            # 标题之后的ol
            ol = category.xpath('following-sibling::ol[1]')
            if ol:
                for li in ol.xpath('li'):
                    article_item = ArticleItem()

                    a = li.xpath('a')
                    if a:
                        title = a.xpath('text()').extract_first()
                        url = a.xpath('@href').extract_first()
                        introduction = ""
                    else:
                        title = li.xpath('p/a/text()').extract_first()
                        url = li.xpath('p/a/@href').extract_first()
                        introduction = li.xpath('p/following-sibling::p[1]/text()').extract_first()

                    print title
                    print url
                    print introduction
                    print weekly_id

                    article_item['category'] = category_name
                    article_item['title'] = title
                    article_item['url'] = url
                    article_item['introduction'] = introduction
                    article_item['weekly_id'] = weekly_id

                    yield article_item
