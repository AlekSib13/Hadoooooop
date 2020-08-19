# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import re
from pprint import pprint
from news_spiders.items import NewsSpidersItem
import datetime

class FoxnewsSpider(scrapy.Spider):
    name = 'foxnews'
    allowed_domains = ['foxnews.com','foxbusiness.com']
    start_urls = ['https://foxnews.com/world']


    def parse(self, response:HtmlResponse):
        #switching between pages: from the main page to main fields, like: politics, business and so on
        titles=response.xpath("//nav[@id]//@href").extract()
        for element in titles:
            if re.findall('politics',element):
                yield response.follow(element,self.politics_page)
            elif re.findall('business',element):
                 element=re.findall('(www.*)',element)[0]
                 element='https://'+element
                 yield response.follow(element,self.business_page)
            if re.findall('world',element):
                 yield response.follow(element,self.world_page)



    def politics_page(self,response:HtmlResponse):
        #searching main news from the page with various politics topics
        main_news_first=response.xpath("//div[contains(@class,'has-hero')]//@href").extract_first()
        main_news_first_link= response.url+re.findall('politics(/.*)',main_news_first)[0]
        yield response.follow(main_news_first_link,self.page_parse)
        main_news_second=response.xpath("//div[contains(@class,'collection-spotlight-cards')][2]//article//h2//@href").extract()
        for element in main_news_second:
            main_news_second_link=response.url+re.findall('politics(/.*)',element)[0]
            yield response.follow(main_news_second_link,self.page_parse)

    def business_page(self,response:HtmlResponse):
        # searching main news from the page with various business topics
        links=response.xpath("//main[@class='main-content']//article/div/a/@href").extract()
        for element in links:
            yield response.follow(element,self.page_parse)

    def world_page(self,response:HtmlResponse):
        # searching main news from the page with various world news topics
        main_news_first_link=response.xpath("//div[contains(@class,'has-hero')]//@href").extract_first()
        yield response.follow(main_news_first_link,self.page_parse)
        main_news_second=response.xpath("//div[contains(@class,'collection-spotlight-cards')][2]//article//h2//@href").extract()
        for element in main_news_second:
            if re.findall('world',str(element)):
                yield response.follow(element,self.page_parse)


    def page_parse(self,response:HtmlResponse):
        #conducting of the information parsing from the page
        link_to_article=response.url
        if re.findall('politics',str(link_to_article)):
             header='Politics'
        elif re.findall('world',str(link_to_article)):
             header='World news'
        else:
             header='Business news'
        topic=response.xpath("//h1/text()").extract()[0]
        publication_date=response.xpath("//div[@class='article-date']//time/text()").extract()[0]
        if re.findall('hours',publication_date):
            hours=int(re.findall('\d+',publication_date)[0])
            publication_date=datetime.datetime.today()-datetime.timedelta(hours=hours)
        tech_key=link_to_article
        # print(link_to_article,header,topic,publication_date,tech_key)
        yield NewsSpidersItem(link_to_article=link_to_article,
                              topic=topic,
                              header=header,
                              publication_date=publication_date,
                              tech_key=tech_key)