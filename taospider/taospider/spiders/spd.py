# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from taospider.items import TaospiderItem

class SpdSpider(scrapy.Spider):
    name = 'spd'
    allowed_domains = ['acm.nyist.net']
    start_urls = ['http://acm.nyist.net/JudgeOnline/status.php?page=1/']


    def parse(self, response):
        self.logger.critical("critical")
        self.logger.error("error")
        self.logger.warning("warning")
        self.logger.info("info")
        self.logger.debug("debug")

        baseurl = "http://acm.nyist.net/JudgeOnline/status.php?do=search&information=userself&result=Accepted&userid="
        usernames = response.selector.xpath("//table[@id='alternate']//td[@class='u-name']//text()").extract() 
        userurls = map(lambda username: baseurl + username.encode("utf8"), usernames)
        userurls = list(set(userurls))
        for userurl in  userurls:
            yield scrapy.Request(url=userurl, callback=self.parseUserAccept)
        pass
        
    def parseUserAccept(self,response):
        lines = response.xpath("//table[@id='alternate']/tbody/tr")
        item=TaospiderItem()
        for line in lines:
            item['user'] = line.xpath("td[@class='u-name']/a/text()").extract()
            item['submit_id'] =line.xpath("td[1]/text()").extract()
            item['question'] = line.xpath("td[3]/a/text()").extract()
            item['time'] = line.xpath("td[last()-2]/text()").extract()
            yield item
        pass
