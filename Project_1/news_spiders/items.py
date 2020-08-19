# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    link_to_article=scrapy.Field()
    topic=scrapy.Field()
    header=scrapy.Field()
    publication_date=scrapy.Field()
    tech_key=scrapy.Field()


class NewsSpidersItem_views(scrapy.Item):
    _id=scrapy.Field()
    date=scrapy.Field()
    date_ts=scrapy.Field()
    tech_key = scrapy.Field()
    views=scrapy.Field()


