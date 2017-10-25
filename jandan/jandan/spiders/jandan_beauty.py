# -*- coding: utf-8 -*-
import scrapy
import pickle
import md5

from jandan.items import JandanItem

black_authors = {u"臀魔"}
white_authors = {u"jxg"}
count = 1
try:
    with open('/home/tao/scrapyspider/jandan/jandan/spiders/downloaded.pkl', 'rb') as pkl_file:
        downloaded = pickle.load(pkl_file)
except Exception,e:
    print("there is no pickle file")
    downloaded = set()


# downloaded = set()  

class JandanBeautySpider(scrapy.Spider):
    name = 'jandan-beauty'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/ooxx/page-225']
    
    # rules = [
    # Rule(LinkExtractor(allow='jandan.net/ooxx/page-\d+',),'parse_new_url',follow=True,),
    # ]

    def __init__(self, *args, **kwargs):
        super(JandanBeautySpider, self).__init__(*args, **kwargs)
        

    def parse(self, response):
        global count
        global downloaded

        self.log("parse url %s" % response.url)
        gallery_list =response.xpath("//ol[@class='commentlist']//div[@class='row']")

        # filter black list authors
        gallery_list = list(filter(lambda x: x.xpath("div[@class='author']/strong/text()")\
            .extract()[0] not in black_authors ,gallery_list))

        # filter bad vote
        gallery_list = list(filter(\
            lambda x: is_not_bad_vote(x.xpath("div[@class='jandan-vote']/span/span/text()").extract()),\
            gallery_list))

        vote_score = list(map(\
            lambda x: getVoteScore(x.xpath("div[@class='jandan-vote']/span/span/text()").extract()), \
            gallery_list))


        image_urls = list(map(\
            lambda x: x.xpath(".//a[@class='view_img_link']/@href").extract()[0][2:].encode("ascii"),\
            gallery_list))

        # only jpg or png
        image_urls = list(filter(lambda x: x.endswith("g"), image_urls))

        for i in range(len(image_urls)):
            item = JandanItem()
            item['url'] = image_urls[i]
            item['score'] = vote_score[i]
            digest = md5.md5(item['url']).hexdigest()
            if digest not in downloaded:
                downloaded.add(digest)
                count += 1
                yield item

                # save progress
                if(count % 50 == 0):
                    print("\n\nsave the progress:\n" + str(count)+"\n\n")
                    with open('/home/tao/scrapyspider/jandan/jandan/spiders/downloaded.pkl', 'wb') as output:
                        pickle.dump(downloaded, output)
            else:
                self.log("there is a downloaded picture!\n")    

        next_url= "http://"+response.xpath('//a[@class="next-comment-page"]//@href')\
                        .extract_first().encode("ascii")[2:]
        yield scrapy.Request(next_url, callback=self.parse)
        


    def closed(self, reason):
        output = open('/home/tao/scrapyspider/jandan/jandan/spiders/downloaded.pkl', 'wb')
        pickle.dump(downloaded, output)

def is_not_bad_vote(vote_list):
    '''
    if oo >= xx return True

    input like:[u'12', u'123']
    return False
    input like:[u'234', u'13']
    return True
    '''
    oo = int(vote_list[0].encode("ascii"))
    xx = int(vote_list[1].encode("ascii"))
    if xx > oo or oo <= 10:
        return False
    else:
        return True

def getVoteScore(vote_list):
    oo = float(vote_list[0].encode("ascii"))
    xx = float(vote_list[1].encode("ascii"))
    return (oo-xx)/oo
