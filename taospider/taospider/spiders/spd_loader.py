# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from taospider.items import TaospiderItem

class SpdSpider(scrapy.Spider):
    name = 'spd_loader'
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
        loader = ItemLoader(item=TaospiderItem(), response=response)
        lines = len(response.xpath("//table[@id='alternate']/tbody/tr"))
        for i in range(lines):
            j=str(i+1)
            loader.replace_xpath('user',"//table[@id='alternate']/tbody/tr["+j+"]/td[@class='u-name']/a/text()")
            loader.replace_xpath('submit_id',"//table[@id='alternate']/tbody/tr["+j+"]/td[1]/text()")
            loader.replace_xpath('question',"//table[@id='alternate']/tbody/tr["+j+"]/td[3]/a/text()")
            loader.replace_xpath('time',"//table[@id='alternate']/tbody/tr["+j+"]/td[last()-2]/text()")
            yield loader.load_item()
