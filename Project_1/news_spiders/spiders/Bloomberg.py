# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import re


class BloombergSpider(scrapy.Spider):
    name = 'Bloomberg'
    allowed_domains = ['bloomberg.com']
    start_urls = ['http://bloomberg.com/europe']

    def parse(self, response:HtmlResponse):
        print(response.text)
        # quick_links=response.xpath("//div[@class='navi-markets-bar']").extract()
        # print(quick_links)
        # for element in quick_links:
        #     if re.findall('Stocks',element):
        #         yield response.follow(element,self.stocks)

        pass


    def stocks(self,response:HtmlResponse):
        print(response.text)
