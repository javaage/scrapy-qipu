import scrapy
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem
from _io import BytesIO
from scrapy.utils.misc import md5sum
import re
import pymysql

class MyFilePipeline(FilesPipeline):
    
    def file_downloaded(self, response, request, info):
        filenames = re.findall(r'filename="(.+)\.pgn"', response.headers['Content-Disposition']);
        hash = filenames[0];
        body = response.body.decode('gbk');
        Event = re.findall(r'Event\s+"(.+)"', body)[0];
        Date = re.findall(r'Date\s+"(.+)"', body)[0];
        RedTeam = re.findall(r'RedTeam\s+"(.+)"', body)[0];
        Red = re.findall(r'Red\s+"(.+)"', body)[0];
        BlackTeam = re.findall(r'BlackTeam\s+"(.+)"', body)[0];
        Black = re.findall(r'Black\s+"(.+)"', body)[0];
        Result = re.findall(r'Result\s+"(.+)"', body)[0];
        ECCO = re.findall(r'ECCO\s+"(.+)"', body)[0];
        Opening = re.findall(r'Opening\s+"(.+)"', body)[0];
        sql = "INSERT INTO qipu (`date`, ecco, result, event, hash, redTeam, red, blackTeam, black, opening) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (Date, ECCO, Result, Event, hash, RedTeam, Red, BlackTeam, Black, Opening); 
        print(sql);
        
        con=pymysql.Connect(host='rm-bp149hof32gt0cewt7o.mysql.rds.aliyuncs.com',port=3306,db='aichess',user='ichess',
                    passwd='Java19786028',charset='utf8')
        cursor=con.cursor()

        try:
            cursor.execute(sql)
            con.commit()
        except:
            con.rollback()
        finally:
            cursor.close()
            con.close()
        
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(hash+'.pgn', buf, info)
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