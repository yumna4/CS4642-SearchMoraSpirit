# import scrapy
# from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
# from scrapy.contrib.spiders import CrawlSpider, Rule
# from scrapy.item import Item, Field
#
# class paperSpider(scrapy.Spider):
#     name = "paperBot"
#
#     # start_urls=['https://moraspirit.com/sports/hockey/maneuvering-balls-victory']
#     # def start_requests(self):
#     #     urls = ['http://moraspirit.com/sports']
#     #     for url in urls:
#     #         yield scrapy.Request(url=url, callback=self.parse)
#
#     start_urls = [
#         'https://moraspirit.com/sports'
#     ]
#
#
#
#     allowed_domains = ["moraspirit.com"]
#
#     # rules = (Rule(SgmlLinkExtractor(), callback='parse_link', follow=False), )
#
#     def parse(self, response):
#
#         links = response.xpath('*//a/@href').extract()
#
#
#         with open("links.txt", 'ab') as f:
#
#             for article in links:
#                 f.write(article)
#                 f.write("\n")
#                 print article
#                 # yield scrapy.Request(article, self.parse_item)
#
#
#         for i in range(2, 90):
#             yield scrapy.Request('http://moraspirit.com/sports?page=%s/' % str(i))
#
#         page = response.url.split("/")[-2]
#         filename = 'paper-%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log('Saved file %s' % filename)
#
#
#     def parse_item(self, response):
#         print "**************************************************************************************"
#         page = response.url.split("/")[-2]
#         filename = 'data/pages/%s.html' % page
#         with open(filename, 'wb') as f:
#             f.write(response.body)
#         self.log('Saved file %s' % filename)
#
#         item = ItemLoader(item=IrprojectItem(), response=response)
#         item.add_xpath(field_name='title', xpath='//div[@class="place-title-box"]/h2/text()')
#         item.add_xpath(field_name='writer', xpath='//p[@class="excerpt"]/text()')
#         item.add_xpath(field_name='editor', xpath='//a[contains(@href,"/cuisine/")]/text()')
#         item.add_xpath(field_name='date', xpath='//a[contains(text(),"Rs.")]/text()')
