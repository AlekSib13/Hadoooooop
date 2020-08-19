# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
import re
from pprint import pprint
from news_spiders.items import NewsSpidersItem


class BbcSpider(scrapy.Spider):
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['https://www.bbc.com/news/world']

    # def parse(self, response:HtmlResponse):
    #     #choice of the most important piece of news from bbc-world:
    #     main_news_first=response.xpath("//a[@class='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold gs-u-mt+ nw-o-link-split__anchor']//@href").extract_first()
    #     link_main='https://www.bbc.com'+main_news_first
    #     yield response.follow(link_main,self.page_parse)
    #     link_business=response.xpath("//li[@class='gs-o-list-ui__item--flush gel-long-primer gs-u-display-block gs-u-float-left nw-c-nav__wide-menuitem-container']//text()").extract()
    #     for element in link_business:
    #         variable='Business'
    #         if re.findall(variable,element):
    #             link_business='https://www.bbc.com/news/'+variable.lower()
    #             print(link_business)
    #             yield response.follow(link_business,self.business_section)
    #     # choice of 5 top news from bbc-world:
    #     main_news_second=response.xpath("//div[contains(@class,'1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m')]//@href").extract()
    #     for element in main_news_second:
    #         if re.findall('\d+',element) and not re.findall('live',element):
    #             # print(element)
    #             link='https://www.bbc.com'+element
    #             # print(link)
    #             yield response.follow(link,callback=self.page_parse)
    #
    #
    # def page_parse(self, response: HtmlResponse):
    #     #parcing info from news
    #     link_to_article=response.url
    #     if re.findall('world',str(link_to_article)):
    #         header='World news'
    #     else:
    #         header='Business'
    #     topic=response.xpath("//h1[@class='story-body__h1']//text()").extract_first()
    #     publication_date=response.xpath("//div[@class='date date--v2']//text()").extract_first()
    #     # print(topic,header,link_to_article,publication_date)
    #     yield NewsSpidersItem(link_to_article=link_to_article,
    #                           topic=topic,
    #                           header=header,
    #                           publication_date=publication_date,
    #                           tech_key=link_to_article)
    #
    #
    # def business_section(self,response:HtmlResponse):
    #     print(response.url)
    #     yield response.follow(response.url,self.parse)


    def parse(self, response:HtmlResponse):
        #choice of the new section, for instance: world, business
        yield response.follow(response.url,callback=self.top_news)
        link=response.xpath("//li[@class='gs-o-list-ui__item--flush gel-long-primer gs-u-display-block gs-u-float-left nw-c-nav__wide-menuitem-container']//text()").extract()
        for element in link:
            if re.findall('Business',element):
                variable_business = 'Business'
                link='https://www.bbc.com/news/'+variable_business.lower()
            elif re.findall('Tech',element):
                variable_tech = 'Technology'
                link = 'https://www.bbc.com/news/' + variable_tech.lower()
            else:
                continue
            yield response.follow(link, callback=self.top_news)
        link_part_world_news=response.xpath("//li[contains(@class,'secondary-menuitem-container')]//@href").extract()
        for element in link_part_world_news:
            if re.findall('europe',element):
                variable_country='europe'
                link_europe_news = 'https://www.bbc.com'+element
                yield response.follow(link_europe_news,callback=self.top_news)

    def top_news(self,response:HtmlResponse):
        #choice of the most important pieces of news from the section:
        main_news_first=response.xpath("//a[@class='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-paragon-bold gs-u-mt+ nw-o-link-split__anchor']//@href").extract_first()
        link_main='https://www.bbc.com'+main_news_first
        yield response.follow(link_main,callback=self.page_parse)
        # choice of 5 top news from bbc-world:
        main_news_second=response.xpath("//div[contains(@class,'1/4@xl gel-1/3@xxl nw-o-keyline nw-o-no-keyline@m')]//@href").extract()
        for element in main_news_second:
            if re.findall('\d+',element) and not re.findall('live',element):
                # print(element)
                link='https://www.bbc.com'+element
                # print(link)
                yield response.follow(link,callback=self.page_parse)


    def page_parse(self, response: HtmlResponse):
        #parcing info from the article
        link_to_article=response.url
        if re.findall('(europe)',str(link_to_article)):
            header='European news'
        elif re.findall('business',str(link_to_article)):
            header='Business news'
        elif re.findall('technology', str(link_to_article)):
            header='Technology news'
        elif re.findall('world',str(link_to_article)):
            header='World news'
        topic=response.xpath("//h1[@class='story-body__h1']//text()").extract_first()
        publication_date=response.xpath("//div[@class='date date--v2']//text()").extract_first()
        yield NewsSpidersItem(link_to_article=link_to_article,
                              topic=topic,
                              header=header,
                              publication_date=publication_date,
                              tech_key=link_to_article)
