from androidweekly.spiders.weekly_spider import WeeklySpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from androidweekly.spiders.article_spider import ArticleSpider
from androidweekly.spiders.weekly_spider import weekly_items
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# settings = get_project_settings()
# process = CrawlerProcess(settings)
# process.crawl(WeeklySpider())
# process.start()

configure_logging()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    yield runner.crawl(WeeklySpider)
    yield runner.crawl(ArticleSpider, items=weekly_items)


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
