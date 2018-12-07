from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.path.dirname(os.path.abspath(__file__))

def execute_detail(clsName):
    execute(["scrapy", "crawl", clsName])

if __name__ =='__main__':
    execute_detail('zhihu')
    pass