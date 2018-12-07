import random
from scrapy_splash import SplashRequest
import json


class UpdateCookies(object):
    qid = ['29240305', '267885696', '22918070', '267885696', '266323557', '34013719', '268275961', '268285564',
           '64854388', '268247495',
           '268241606', '268275961', '268155387', '35787067', '26193468', '22918070', '37204212', '267439583',
           '20684684', '20684684',
           '53670796', '26613082', '23181351', '52107943', '265664960', '268119125', '268115073', '26613082',
           '36688754', '266639322']

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        'X-Crawlera-Cookies': 'disable'
    }

    def __init__(self,func):
        self.func = func

    def __call__(self, *args, **kwargs):
        # 调用函数前做一遍cookie的更新
        self.request_cookies()
        self.func(*args,**kwargs)

    def request_cookies(self):
        url = ['https://www.zhihu.com/question/'+ i for i in self.qid]
        # 此函数更新cookie
        lua_get_cookie = """
                            function main(splash)
                                local cookies = ""
                                splash:on_response_headers(function(response)
                                    local response_cookies = response.headers['Set-Cookie']
                                    cookies= cookies .. response_cookies
                                end)
                                assert(splash:go(splash.args.url))
                                return {cookies,splash:html()}
                            end
                            """
        yield SplashRequest(url=url[random.randint(0,len(url)-1)], endpoint='execute', headers=self.headers,
                            callback=self.update_cookies,args={'wait': 2, 'lua_source': lua_get_cookie, 'url': url[random.randint(0,len(url)-1)]})


    def update_cookies(self,response):
        data = json.loads(response.text)
        cookie_data = data['1']
        res_html = data['2']
        print(cookie_data)
