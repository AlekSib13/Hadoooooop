# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import engine, create_engine,Table,column,ForeignKey,MetaData,Column,Integer,VARCHAR,NVARCHAR
from sqlalchemy.sql import and_,or_,between,update,delete,insert,select
from sqlalchemy.orm import sessionmaker
import re


metadata=MetaData()
news_detailed_info=Table('news_detailed_info',metadata,
                        Column('_id',Integer,primary_key=True),
                        Column('link',VARCHAR(4096)),
                        Column('topic',NVARCHAR(2000)),
                        Column('header',NVARCHAR(2000)),
                        Column('publication_date',VARCHAR(512)),
                        Column('tech_key',VARCHAR(512),unique=True))

number_of_views=Table('news_views',metadata,
                      Column('_id',Integer,primary_key=True),
                      Column('views',VARCHAR(1024)),
                      Column('tech_key',VARCHAR(512)))

rbc_views = Table('rbc_news_views', metadata,
                  Column('_id', Integer, primary_key=True),
                  Column('date', VARCHAR(512)),
                  Column('date_ts', VARCHAR(512)),
                  Column('tech_key', VARCHAR(512)),
                  Column('views', VARCHAR(512)))



class NewsSpidersPipeline:
    def __init__(self):
        engine=create_engine('mysql+mysqlconnector://root:Ub19_%401@localhost:3306/news',echo=True)
        self.conn=engine.connect()

    def process_item(self, item, spider):
        if spider.name=='rbc':
            return self.changer_1(item)
        if spider.name=='rbc_stats':
            return self.changer_2(item)
        if spider.name=='bbc' or spider.name=='foxnews':
            return self.loader_3(item)


    def changer_1(self,info):
            info['header']=info['header'][0]
            info['publication_date']=info['publication_date'][0]
            info['topic']=info['topic'][0]
            return self.loader_1(info)


    def loader_1(self, info):
        print(info)
        self.conn.execute(news_detailed_info.insert(),
                          [{'link': info['link_to_article'],
                            'topic': info['topic'],
                            'header': info['header'],
                            'publication_date': info['publication_date'],
                            'tech_key': info['tech_key']}])



    def changer_2(self, info):
        info['date']=re.findall('date":"(.+)",',str(info['date']))[0]
        info['date_ts']=re.findall('date_ts":(\d+)',str(info['date_ts']))[0]
        info['views'] = re.findall('"show":(\d*)', str(info['views']))[0]
        return self.loader_2(info)

    def loader_2(self,info):
        print(info)
        self.conn.execute(rbc_views.insert(),
                          [{'date':info['date'],
                            'date_ts':info['date_ts'],
                            'tech_key': info['tech_key'],
                            'views': info['views']}])



    def loader_3(self,info):
        #load news from bbc-world, foxnews into mysql database
        print(info)
        if info['topic']!=None:
            self.conn.execute(news_detailed_info.insert(),
                              [{'link':info['link_to_article'],
                               'topic':info['topic'],
                               'header':info['header'],
                               'publication_date':info['publication_date'],
                                'tech_key':info['tech_key']}])



### старый код:
    # def changer_2(self, info):
    #     info['views'] = re.findall('"show":(\d*)', str(info['views'][0]))[0]
    #     return self.loader_2(info)

    # def loader_2(self,info):
    #     print(info)
    #     self.conn.execute(number_of_views.insert(),
    #                       [{'views': info['views'],
    #                         'tech_key': info['tech_key']}])