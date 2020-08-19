# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from test import extract_links
import re
from news_spiders.pipelines import engine
from sqlalchemy import engine, create_engine,Table,column,ForeignKey,MetaData,Column,Integer,VARCHAR,NVARCHAR
from sqlalchemy.sql import and_,or_,between,update,delete,insert,select


class TestSpiderSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['rbc.ru']
    start_urls = ['http://rbc.ru/']

    def parse(self, response:HtmlResponse):
        links=[]
        for link in extract_links():
            yield response.follow(link,self.parse_page)
        pass

    def parse_page(self,response:HtmlResponse):
        date=re.findall('date":"(.+)",',response.text)[0]
        date_ts=re.findall('date_ts":(\d+)',response.text)[0]
        tech_key = response.url
        views=re.findall('show":(\d*)',response.text)[0]
        print(response.text,date,date_ts,views)
        pass
