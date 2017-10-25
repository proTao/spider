# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TaospiderPipeline(object):
    def process_item(self, item, spider):
        keys = item.keys()
        for key in keys:
            item[key] = item[key][0].encode('utf8').strip() 
        return item
