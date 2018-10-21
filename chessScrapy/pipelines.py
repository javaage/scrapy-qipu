# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem

class ChessscrapyPipeline(FilesPipeline):
    def process_item(self, item, spider):

    	#file_urls

    	# print('FilesPipeline1');
    	# print(self);
    	# print(item);
    	# print(spider);
        return item

    def get_media_requests(self, item, info):
        print('FilesPipeline2');
        print(item);
        for file_url in item['file_urls']:
            yield scrapy.Request(file_url)

    def item_completed(self, results, item, info):
        print('FilesPipeline3');
        print(item);
        file_paths = [x['path'] for ok, x in results if ok]
        if not file_paths:
            raise DropItem("Item contains no images")
        item['file_paths'] = file_paths
        return item

    def file_path(self, request, response=None, info=None): 
        print('get file name');
        print(request.url);
        path = urlparse(request.url).path 
        return join(basename(dirname(path)),basename(path))