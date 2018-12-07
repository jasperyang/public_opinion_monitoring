# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import pymysql
import urllib.parse
import json
import datetime
import pymysql
from YQ_spider.items import BaiduDataApiItem

class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['120.76.205.241:8000']
    start_urls = ['http://120.76.205.241:8000/page/baidu?apikey=h0PEpVhm4ODEM3pikBgTy9qYHNmIiuvkKuBkiJL6ojcCqAr0W49tXFuw6FRRmK1Q&kw=']
    today = datetime.datetime.today().date()

    headers = {
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }

    def start_requests(self):
        conn = pymysql.connect(host='rm-bp1ppxouwgu9ta1787o.mysql.rds.aliyuncs.com', port=3306, user='root',password='YKYroot123123', db='scrapyhub', charset='utf8')
        cur = conn.cursor()
        cur.execute("select monitor_word from monitor_search_word group by monitor_word")
        word_list = cur.fetchall()
        word_list = [i[0] for i in word_list]
        url_list = [self.start_urls[0] + urllib.parse.quote(i) for i in word_list]

        for url in url_list:
            yield Request(url=url,headers=self.headers,callback=self.parse)

        #yield Request(url=url_list[0], headers=self.headers,callback=self.parse)

    def parse(self, response):
        title = []
        url = []
        parentAppCode = []
        data = json.loads(response.text)
        kw = response.url.split("&")[1]
        kw = kw.replace("kw=", "")
        kw = urllib.parse.unquote(kw)
        content_flag = 'false'
        if (data['retcode'] == '000000'):
            content_flag = 'true'
            data_obj = data['data']
            length = len(data_obj)
            for row in range(0, length):
                content = data_obj[row]
                title.append(content['title'].encode('utf-8'))
                url.append(content['url'])
                parentAppCode.append(content['parentAppCode'])
        elif (data['retcode'] == '100002'):
            print('已加载完数据...')
        else:
            print(str(kw)+'数据出错')
        if (content_flag == 'true'):
            iterm = BaiduDataApiItem()
            iterm['title'] = title
            iterm['url']= url
            iterm['parentAppCode']= parentAppCode
            iterm['search_word'] = kw.encode('utf-8')
            iterm['spider_date'] = self.today
            iterm['table_name'] = 'leo_baidu'
            return iterm
