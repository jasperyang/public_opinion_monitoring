# -*- coding: utf-8 -*-
import scrapy
import datetime
import pymysql
import urllib.parse
from YQ_spider.items import ToutiaoDataApiItem,ToutiaoDateDataApiItem
from scrapy_splash import SplashRequest
import re

class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    start_urls = ['https://www.toutiao.com/search/?keyword=']
    today = datetime.datetime.today().date()
    headers={
        "Accept-Encoding": "",
        "Connection": "",
        "cookie":'tt_webid=75253443220; UM_distinctid=1611b8c7184cc9-01760b9af29b4e-32677403-fa000-1611b8c7185cf2; WEATHER_CITY=%E5%8C%97%E4%BA%AC; uuid="w:3ae4d667d2d74b0bb6f88c9730bfe70f"; _ga=GA1.2.1300945078.1519468575; sso_login_status=1; login_flag=0658a4f315615da2e93133051afc4322; sessionid=1182ab3b4b8b4c34291439a96cbb3e4f; uid_tt=40ffeb77a4a9d9c306930f884ec73c02; sid_tt=1182ab3b4b8b4c34291439a96cbb3e4f; sid_guard="1182ab3b4b8b4c34291439a96cbb3e4f|1521518053|15552000|Sun\054 16-Sep-2018 03:54:13 GMT"; cp=5AB8ECDD8FF9BE1; tt_webid=75253443220; tt_webid=75253443220; CNZZDATA1259612802=1623093824-1516581967-%7C1522138894; __tasessionId=z3asgc7cp1522139927777',
        "referer":"https://www.toutiao.com/",
        "user-agent":"Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36"
    }

    http_user = 'f5b9c77aacfa496bac573c3cf548c9ac'



    def start_requests(self):
        conn = pymysql.connect(host='rm-bp1ppxouwgu9ta1787o.mysql.rds.aliyuncs.com', port=3306, user='root',password='YKYroot123123', db='scrapyhub', charset='utf8')
        cur = conn.cursor()
        cur.execute("select monitor_word from monitor_search_word group by monitor_word")
        word_list = cur.fetchall()
        word_list = [i[0] for i in word_list]
        url_list = [self.start_urls[0] + urllib.parse.quote(i) for i in word_list]
        """
        for url in url_list:
            yield SplashRequest(url=url, headers=self.headers, callback=self.parse, args={'wait': 2})
        """
        yield SplashRequest(url=url_list[0],headers=self.headers, callback=self.parse,args={'wait': 2})

    def text_extract(self,tList):
        tList = [re.findall('>.*?<', i) for i in tList]
        tList = ["".join(i) for i in tList]
        tList = [re.sub("[<>]", "", i) for i in tList]
        return tList


    def parse(self, response):
        iterm = ToutiaoDataApiItem()
        kw = response.url.split("?")[1]
        kw = urllib.parse.unquote(kw.replace("keyword=", ""))
        title = response.css('div.normal.rbox > div > div.title-box > a > span').extract()
        title = self.text_extract(title)
        href = response.css('div.normal.rbox > div > div.title-box > a::attr(href)').extract()
        url = ['https://www.toutiao.com'+i for i in href]
        publisher = response.css('div.normal.rbox > div > div.y-box.footer > div > div > a.lbtn.source.J_source').extract()
        publisher = self.text_extract(publisher)
        publisher = [i.strip().replace('\xa0', '') for i in publisher]
        iterm['title']= title
        iterm['url'] = url
        iterm['publisher'] = publisher
        iterm['search_word'] = kw
        iterm['spider_date'] = self.today
        iterm['table_name'] = 'leo_toutiao'
        yield iterm
        headers = {
            "Accept-Encoding": "",
            "Connection": "",
            "cookie": 'tt_webid=75253443220; UM_distinctid=1611b8c7184cc9-01760b9af29b4e-32677403-fa000-1611b8c7185cf2; WEATHER_CITY=%E5%8C%97%E4%BA%AC; uuid="w:3ae4d667d2d74b0bb6f88c9730bfe70f"; _ga=GA1.2.1300945078.1519468575; sso_login_status=1; login_flag=0658a4f315615da2e93133051afc4322; sessionid=1182ab3b4b8b4c34291439a96cbb3e4f; uid_tt=40ffeb77a4a9d9c306930f884ec73c02; sid_tt=1182ab3b4b8b4c34291439a96cbb3e4f; sid_guard="1182ab3b4b8b4c34291439a96cbb3e4f|1521518053|15552000|Sun\054 16-Sep-2018 03:54:13 GMT"; cp=5AB8ECDD8FF9BE1; tt_webid=75253443220; tt_webid=75253443220; CNZZDATA1259612802=1623093824-1516581967-%7C1522138894; __tasessionId=z3asgc7cp1522139927777',
            "referer": "https://www.toutiao.com/",
            "user-agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8"
            }
        for num in range(0,len(title)):
            next_title = title[num]
            next_url = url[num]
            yield SplashRequest(url=next_url,headers=headers, callback=self.parse_redirect,endpoint='render.html',meta = {"title": next_title,"splash":{"dont_process_response":True}},args={'wait': 2})


    def parse_redirect(self,response):
        title = response.meta.get("title")
        text = response.text
        try:
            a_id = re.search('.*group_id.*?(\d+)";',str(text)).group(1)
            headers = {
                "Accept-Encoding": "",
                "Connection": "",
                "cookie": 'tt_webid=75253443220; UM_distinctid=1611b8c7184cc9-01760b9af29b4e-32677403-fa000-1611b8c7185cf2; WEATHER_CITY=%E5%8C%97%E4%BA%AC; uuid="w:3ae4d667d2d74b0bb6f88c9730bfe70f"; _ga=GA1.2.1300945078.1519468575; sso_login_status=1; login_flag=0658a4f315615da2e93133051afc4322; sessionid=1182ab3b4b8b4c34291439a96cbb3e4f; uid_tt=40ffeb77a4a9d9c306930f884ec73c02; sid_tt=1182ab3b4b8b4c34291439a96cbb3e4f; sid_guard="1182ab3b4b8b4c34291439a96cbb3e4f|1521518053|15552000|Sun\054 16-Sep-2018 03:54:13 GMT"; cp=5AB8ECDD8FF9BE1; tt_webid=75253443220; tt_webid=75253443220; CNZZDATA1259612802=1623093824-1516581967-%7C1522138894; __tasessionId=z3asgc7cp1522139927777',
                "referer": "https://www.toutiao.com/",
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
                "upgrade-insecure-requests":"1",
                "cache-control":"max-age=0"
            }

            url = "https://www.toutiao.com/a"+str(a_id)
            yield SplashRequest(url=url, headers=headers, callback=self.parse_detail, endpoint='render.html',meta={"title": title}, args={'wait': 2})
        except:
            iterm = ToutiaoDateDataApiItem()
            iterm['title'] = title
            iterm['publish_date'] = 'null'
            iterm['spider_date'] = self.today
            iterm['table_name'] = 'leo_toutiao_date'
            yield iterm

    def parse_detail(self,response):
        text = response.text
        try:
            date = re.search(".*time.{3}(\d{4}-\d{2}-\d{2}).*",str(text)).group(1)
        except:
            date = 'null'
        title = response.meta.get("title")
        iterm = ToutiaoDateDataApiItem()
        iterm['title'] = title
        iterm['publish_date'] = date
        iterm['spider_date'] = self.today
        iterm['table_name'] = 'leo_toutiao_date'
        yield iterm







