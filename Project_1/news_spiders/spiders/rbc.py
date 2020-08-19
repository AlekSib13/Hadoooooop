# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from news_spiders.items import NewsSpidersItem
from news_spiders.items import NewsSpidersItem_views
import re



class RbcSpider(scrapy.Spider):
    name = 'rbc'
    allowed_domains = ['rbc.ru','https://www.rbc.ru/redir/stat/']
    start_urls = ['http://rbc.ru/']

    # Добавить заход паука в url по политике и экономике (так как сейчас написано в url - не работает)




    def parse(self, response:HtmlResponse):
        main_news = response.xpath("//span[@class='main__big__text-wrap']/parent::a/@href").extract_first()
        yield response.follow(main_news,callback=self.news_details)
        news=response.xpath("//span[@class='main__feed__title-wrap']/parent::a/@href").extract()
        for piece_of_news in news:
            print(type(piece_of_news))
            yield response.follow(piece_of_news,callback=self.news_details)
        more_news= response.xpath("//div[@class='tabs__item js-index-tabs']//@href").extract()
        for element in more_news:
            yield response.follow(element,callback=self.more_news_list)


    def more_news_list(self,response:HtmlResponse):
        news=response.xpath("//div[contains(@class,'load-container')]//@href").extract()
        for piece_of_news in news:
            yield response.follow(piece_of_news,callback=self.news_details)


    def news_details(self, response: HtmlResponse):
        link = response.xpath("(//div[contains(@class,'js-rbcslider-slide rbcslider')])[1]/@data-shorturl").extract()
        tech_key=re.findall('.ru/(.*[^]\'])',str(link))
        tech_key='https://www.rbc.ru/redir/stat/'+tech_key[0]
        # yield response.follow(tech_key,callback=self.views_number)
        link_to_article=response.xpath("(//meta[@property='og:url'])[1]/@content").extract_first()
        topic=response.xpath("(//div[@class='article__header__info-block']/child::a)[1]//text()").extract()
        header = response.xpath("(//h1)[1]//text()").extract()
        publication_date=response.xpath("(//span[@class='article__header__date'])[1]/text()").extract()
        # full_article=response.xpath("(//div[@class='article__text article__text_free'])[1]//text()").extract()
        # print(link_to_article,topic,header,publication_date,tech_key)
        yield NewsSpidersItem(link_to_article=link_to_article,topic=topic,header=header, publication_date=publication_date,tech_key=tech_key)

    # def views_number(self,response:HtmlResponse):
    #     views=response.xpath('//body//text()').extract()
    #     tech_key=re.findall('<200(.*)>',str(response))[0]
    #     print(tech_key,views)
    #     yield NewsSpidersItem_views(views=views,tech_key=tech_key)

