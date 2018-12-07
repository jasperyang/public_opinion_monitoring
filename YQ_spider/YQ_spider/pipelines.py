# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime

import sys
sys.path.append("../")
import config

class DateEncoder(json.JSONEncoder ):  
    def default(self, obj):  
        if isinstance(obj, type(datetime.today().date())):  
            return obj.__str__()  
        if isinstance(obj, bytes):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)  

class DataApiPipeline(object):
    def __init__(self):
        # self.conn = pymysql.connect(host='rm-bp1ppxouwgu9ta1787o.mysql.rds.aliyuncs.com', port=3306, user='root', password='YKYroot123123', db='scrapyhub', charset='utf8')
        return
    
    def return_columns_s(self, num):
        p = '%s'
        num =int(num)
        while num > 1:
            p += ',%s'
            num -= 1
        return p

    def return_iterm_value(self,iterm):
        del iterm['table_name']
        iterm_name = ",".join(list(iterm.keys()))
        if isinstance(iterm[list(iterm.keys())[0]],list):
            len_num = len(iterm[list(iterm.keys())[0]])
            if "search_word" in iterm_name:
                iterm['search_word'] = [iterm['search_word'] for i in range(len_num)]
            if "spider_date" in iterm_name:
                iterm['spider_date'] = [iterm['spider_date'] for i in range(len_num)]
            iterm_value_list = []
            for num in range(0,len_num):
                iterm_value = [iterm[i][num] for i in list(iterm.keys())]
                iterm_value = tuple(iterm_value)
                iterm_value_list.append(iterm_value)
        else:
            iterm_value = [iterm[i] for i in list(iterm.keys())]
            iterm_value = tuple(iterm_value)
            iterm_value_list = [iterm_value]
        return iterm_name,iterm_value_list

    def process_item(self, item, spider):
        # cur = self.conn.cursor()
        # table_name = item['table_name']
        # item_name,item_value = self.return_iterm_value(item)
        # p = self.return_columns_s(len(list(item.keys())))
        # sql = "INSERT INTO {}({}) VALUES({})".format(table_name,item_name,p)
        # cur.executemany(sql,item_value)
        # self.conn.commit()
        jsontext=json.dumps(dict(item),ensure_ascii=False,cls=DateEncoder) + '\n'
        outfile = open(config.item_json,'wb')
        outfile.write(jsontext.encode("utf-8"))
        outfile.close()
        return item
