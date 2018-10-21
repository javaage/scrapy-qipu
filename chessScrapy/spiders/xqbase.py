# -*- coding: utf-8 -*-
import scrapy
from MatpItem import MatpItem

class XqbaseSpider(scrapy.Spider):
    name = 'xqbase'
    allowed_domains = ['xqbase.com']
    start_urls = ['http://www.xqbase.com/']

    def start_requests(self):
        for i in range(1,2): #12142
        	url = 'http://www.xqbase.com/xqbase/?gameid=%d' % (i);
        	yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        link = response.xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[4]/td/p/a[4]/@href').extract_first();
        print(link);
        if link:
            yield scrapy.Request(response.urljoin(link),callback=self.parse_link)
        
        # print(self);
        # print(response);
        #/html/body/table/tbody/tr/td[2]/table/tbody/tr[4]/td/p/a[4]
#         for xcontent in response.xpath('/html/body/table/tbody/tr/td[2]/table/tbody/tr[4]/td/p'):
#             title = xcontent.xpath('a[1]/font/text()').extract_first();
#             date = xcontent.xpath('a[2]/font/text()').extract_first();
#             link = xcontent.xpath('a[4]/@href').extract_first();
            # print(title);
            # print(link);
            # print(response.urljoin(link));
            #yield response.follow(link, self.parse)
            # yield {'title': title, 'date': date}
#             yield scrapy.Request(response.urljoin(link),callback=self.parse_link)

        # for next_page in response.css('div.prev-post > a'):
        #     yield response.follow(next_page, self.parse)
    def parse_link(self,response): 
        # href = response.css('a.reference.external::attr(href)').extract_first() 
        # url = response.urljoin(href) 
#         print(response.url);
#         print(response.status);
#         print(response.headers);
#         print(response.body);
#         print(response.request);
#         print(response.meta);
#         print(response.flags);
        matpl = MatpItem()
        matpl['file_urls'] = [response.url]
        return matpl