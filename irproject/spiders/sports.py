import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from irproject.items import IRProjectItem
import json



with open("links.txt", 'rb') as f:
    content = f.readlines()
links = [x.strip() for x in content]
articles=[]

for i in links:
    words=i.split('/')
    if len(words)>3:
        if words[1]=='sports' or words[1]=='features':
            articles.append("https://moraspirit.com"+i)
i=0
articles=list(set(articles))
articles=[i.split() for i in articles]

articles=articles[1:10]
class paperSpider(scrapy.Spider):
    name = "sportsBot"

    start_urls=articles[0]
    print start_urls
    allowed_domains = ["moraspirit.com"]

    # rules = (Rule(SgmlLinkExtractor(), callback='parse_item', follow=False), )

    def parse(self, response):


        item = ItemLoader(item=IRProjectItem(), response=response)

        item.add_value(field_name='title', value=response.xpath('/html/body/div[1]/div/div/div/div[2]/div/div/div/div/h1/text()').extract())
        credentialsParaNumber=len(response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p'))
        item.add_value(field_name='credentials',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p[%s]/text()'%credentialsParaNumber).extract())
        item.add_value(field_name='date',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/span/text()').extract())

        # item.add_value(field_name='rating',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[4]/div[2]/div/form/div/div/div/div/div[2]/div/span[2]/span').extract())
        # item.add_value(field_name='reads',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[3]/div/ul/li/span').extract())
        # item.add_value(field_name='',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/span/text()').extract())
        # item.add_value(field_name='likes',value=response.xpath('/text()').extract())
        # item.add_value(field_name='tweets',value=response.xpath('/text()').extract())
        # item.add_value(field_name='',value=response.xpath('/text()').extract())
        # item.add_value(field_name='',value=response.xpath('/text()').extract())


        with open("scrapedDetails.json", 'ab') as f:
            line = json.dumps(dict(item.load_item())) + "\n"
            f.write(line)
        #     f.write(item.load_item())

        yield item.load_item()

        for i in articles[1:]:
            yield scrapy.Request(i[0])


# '/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p[6]/strong/text()'
# '/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p[15]/text()'
