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
articles=articles[100:150]
# for i in articles:
#     print i
#     print ""
#     print ""
#     print ""

class paperSpider(scrapy.Spider):
    name = "sportsBot"

    start_urls=articles[0]
    print start_urls
    allowed_domains = ["moraspirit.com"]

    # rules = (Rule(SgmlLinkExtractor(), callback='parse_item', follow=False), )

    def parse(self, response):




        dateStuff=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/span/text()').extract()
        date=dateStuff[0].split(' ')[2]


        body=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div').extract()
        body=str(body).replace("<strong>","").replace("</strong>","").split('<p>')
        credentialsStuff=body[-4:]
        credentialsStuff.reverse()
        # for i in credentialsStuff:
        #     print i
        #     print "#################"
        # print "@@@@@@@@@@@@@@@@@@@@"
        credentialsStuff=' '.join(credentialsStuff).split('<')

        author=""
        editor=""
        sponsor=""
        for j in range (len(credentialsStuff)):
            i=credentialsStuff[j]
            # print i
            # print "&&&&&&&"
            if 'Article by' in i :
                if ":" in i:
                    author=i.split(': ')[-1]
                if "-" in i:
                    author=i.split('- ')[-1]
            elif "By" in i:
                if len(i)>10:
                    author=" ".join(i.split(" ")[-2:])
                else:
                    author=credentialsStuff[j+1].split("> ")[-1]

            if 'Edited by' in i :
                if ":" in i:
                    editor=i.split(': ')[-1]
                if "-" in i:
                    editor=i.split('- ')[-1]
            if 'Sponsored by' in i:
                if ":" in i:
                    sponsor=i.split(': ')[-1]
                if "-" in i:
                    sponsor=i.split('- ')[-1]
        print author
        print editor
        print type(editor)
        print sponsor
        print "*********************"
        item = ItemLoader(item=IRProjectItem(), response=response)
        empty=True
        if author!="":
            empty=False
            item.add_value(field_name='author',value=author.replace("\\xa0","").replace("em>","").replace("\\n",""))
            item.add_value(field_name='editor',value=editor)
            item.add_value(field_name='sponsor',value=sponsor)
            item.add_value(field_name='date',value=date)
            title=response.xpath('/html/body/div[1]/div/div/div/div[2]/div/div/div/div/h1/text()').extract()
            title=str(title)
            if "\u" in title:
                num=title.split("\u")[1]
                num=num[0:4]
                uni="\u"+num
                title=title.replace(uni,uni.encode('utf-8'))
                print type(title)
            # title=' '.join([i.encode for i in title.split(" ")])
            item.add_value(field_name='title', value=title)

        with open("scrapedDetails1.json", 'ab') as f:
            if not empty:
                line = json.dumps(dict(item.load_item())) + "\n"
                f.write(',')
                f.write(line)
    #     f.write(item.load_item())

        yield item.load_item()

        for i in articles[1:]:
            yield scrapy.Request(i[0])



        print "end"

        # credentialsParaNumber=len(response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p'))
        # item.add_value(field_name='credentials',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p[%s]/text()'%credentialsParaNumber).extract())

        #
        # # item.add_value(field_name='rating',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[4]/div[2]/div/form/div/div/div/div/div[2]/div/span[2]/span').extract())
        # # item.add_value(field_name='reads',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[3]/div/ul/li/span').extract())
        # # item.add_value(field_name='',value=response.xpath('/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[1]/span/text()').extract())
        # # item.add_value(field_name='likes',value=response.xpath('/text()').extract())
        # # item.add_value(field_name='tweets',value=response.xpath('/text()').extract())
        # # item.add_value(field_name='',value=response.xpath('/text()').extract())
        # # item.add_value(field_name='',value=response.xpath('/text()').extract())
        #
        #



# '/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p[6]/strong/text()'
# '/html/body/div[1]/div/div/div/div[3]/div[2]/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div[3]/div/div/p[15]/text()'
