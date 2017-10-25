# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jandan import settings
import os
import urllib
import scrapy

class JandanPipeline(object):
    def process_item(self, item, spider):
        dir_path = "/home/tao/scrapyspider/jandan/download"
        
        file_name = str(item['score']) + "_" + item['url'][-8:-4] + item['url'][-4:]
        file_path = '%s/%s' % (dir_path,file_name)

        with open(file_path,'wb') as file_writer:
            conn = urllib.urlopen("http://"+item['url'])#下载图片
            file_writer.write(conn.read())
        file_writer.close()
        return item
