# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaospiderItem(scrapy.Item):
    # define the fields for your item here like:
    user = scrapy.Field()
    question = scrapy.Field()
    submit_id = scrapy.Field()
    time = scrapy.Field()
    pass
