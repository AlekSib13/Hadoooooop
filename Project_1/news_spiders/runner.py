from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from news_spiders import settings
from news_spiders.spiders.rbc import RbcSpider
from news_spiders.spiders.rbc_stats import RbcStatsSpider
from news_spiders.spiders.bbc import BbcSpider
from news_spiders.spiders.Bloomberg import BloombergSpider
from news_spiders.spiders.foxnews import FoxnewsSpider
from news_spiders.spiders.test_spider import TestSpiderSpider



if __name__=="__main__":
    spider_settings=Settings()
    spider_settings.setmodule(settings)

    spider_process=CrawlerProcess(settings=spider_settings)
    spider_process.crawl(RbcSpider)
    spider_process.crawl(RbcStatsSpider)
    spider_process.crawl(BbcSpider)
    spider_process.crawl(FoxnewsSpider)
    # spider_process.crawl(BloombergSpider)
    # spider_process.crawl(TestSpiderSpider)

    spider_process.start()

