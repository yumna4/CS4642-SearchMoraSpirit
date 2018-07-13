# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IRProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    credentials=scrapy.Field()
    date=scrapy.Field()
    rating=scrapy.Field()
    reads=scrapy.Field()
    pass