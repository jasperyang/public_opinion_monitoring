# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import os
import urllib.parse
import json
import datetime
from YQ_spider.items import DataApiItem

import sys
sys.path.append("../../")
import config



class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['120.76.205.241:8000']
    start_urls = ['http://120.76.205.241:8000/post/weibo?apikey=h0PEpVhm4ODEM3pikBgTy9qYHNmIiuvkKuBkiJL6ojcCqAr0W49tXFuw6FRRmK1Q&kw=']
    today = datetime.datetime.today().date()
    # path:/Users/yky/github/data_api/data_api
    path = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

    headers={
        "Accept-Encoding": "gzip",
        "Connection": "close"
    }

    def start_requests(self):
        # conn= pymysql.connect(host='rm-bp1ppxouwgu9ta1787o.mysql.rds.aliyuncs.com', port=3306, user='root', password='YKYroot123123', db='scrapyhub', charset='utf8')
        # cur = conn.cursor()
        # cur.execute("select monitor_word from monitor_search_word group by monitor_word")
        # word_list=cur.fetchall()
        # word_list=[i[0] for i in word_list]
        
        # 从文件中获取关键词 : /Users/yangyi/Desktop/work_in_keep/public_opinion_monitoring/YQ_spider/YQ_spider
        key_file = open(config.keyword_in_scrapy)
        word_list = []
        line = key_file.readline().strip().split(' ')
        for word in line:
            if word != '':
                word_list.append(word)
        url_list = [self.start_urls[0] + urllib.parse.quote(i) for i in word_list]

        for url in url_list:
            yield Request(url=url,headers=self.headers,callback=self.parse)

        #yield Request(url=url_list[0],headers=self.headers, callback=self.parse)


    def parse(self, response):
        v_content = []
        v_readview = []
        v_date = []
        v_postname = []
        commentCount = []
        post_url = []
        shareCount = []
        likeCount = []
        user_link = []
        fansCount = []
        content_flag = 'false'
        data = json.loads(response.text)
        kw = response.url.split("&")[1]
        kw = kw.replace("kw=","")
        kw = urllib.parse.unquote(kw)
        if (data['retcode'] == '000000'):
            content_flag = 'true'
            data_obj = data['data']
            length = len(data_obj)
            for row in range(0, length):
                content = data_obj[row]
                v_content.append(content['content'])
                v_readview.append(content['viewCount'])
                v_date.append(content['publishDateStr'][0:10])
                v_postname.append(content['from']['name'])
                commentCount.append(content['commentCount'])
                post_url.append(content['url'])
                shareCount.append(content['shareCount'])
                likeCount.append(content['likeCount'])
                user_link.append(content['from']['url'])
                fansCount.append(content['from']['fansCount'])
        elif (data['retcode'] == '100002'):
            print('已加载完数据...')
        else:
            print(str(kw)+'数据出错')
        if (content_flag == 'true'):
            iterm =DataApiItem()
            iterm['content'] = v_content
            iterm['readView'] = v_readview
            iterm['dt'] = v_date
            iterm['commentCount'] = commentCount
            iterm['postUrl'] = post_url
            iterm['shareCount'] = shareCount
            iterm['likeCount'] = likeCount
            iterm['userLink'] = user_link
            iterm['fansCount'] = fansCount
            iterm['postName'] = v_postname
            iterm['search_word'] = kw.encode('utf-8')
            iterm['spider_date'] = self.today
            iterm['table_name'] = 'leo_weibo'
            yield iterm


