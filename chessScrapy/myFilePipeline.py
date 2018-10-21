import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from _io import BytesIO
from scrapy.utils.misc import md5sum
import re

class MyFilePipeline(FilesPipeline):
    
    def file_downloaded(self, response, request, info):
        filenames = re.findall(r'filename="(.+)"', response.headers['Content-Disposition']);
        path = filenames[0];
        #path = self.file_path(request, response=response, info=info)
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)
        return checksum

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.files_result_field in item.fields:
            item[self.files_result_field] = [x for ok, x in results if ok]
        return item
    
    def file_path(self, request, response=None, info=None):
#         path = urlparse(request.url).path
#         path = join(basename(dirname(path)),basename(path))
#         return path
        return request.url;