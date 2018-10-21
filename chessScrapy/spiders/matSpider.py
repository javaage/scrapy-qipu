# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractor import LinkExtractor
from MatpItem import MatpItem

class MatSpider(scrapy.Spider):
    name = "mat"
    allowed_domains = ["matplotlib.org"]
    start_urls = ['https://matplotlib.org/examples']

    def parse(self, response):
        link = LinkExtractor(restrict_css='div.toctree-wrapper.compound li.toctree-l2')
        for link in link.extract_links(response):
            yield scrapy.Request(url=link.url,callback=self.example)

    def example(self,response):
        href = response.css('a.reference.external::attr(href)').extract_first()
        url = response.urljoin(href)
        example = MatpItem()
        example['file_urls'] = [url]
        return example