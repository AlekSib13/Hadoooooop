# -*- coding: utf-8 -*-
import scrapy


class TsargradSpider(scrapy.Spider):
    name = 'tsargrad'
    allowed_domains = ['tsargrad.tv']
    start_urls = ['http://tsargrad.tv/']

    def parse(self, response):
        pass
