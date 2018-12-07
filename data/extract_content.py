#!/usr/bin/env python
# coding=utf-8

import json
import os
import re
import sys
sys.path.append("..")
import config

def get_filenames_dir(file_dir):
    filenames = []
    for root, dirs, files in os.walk(file_dir):
        for i in range(len(files)):
            filenames.append(root + '/' + files[i])
    return filenames


def Reverse_chinese(_str):
    line = _str.strip()  # 处理前进行相关的处理，包括转换成Unicode等pwd
    p2 = re.compile(r'[^\u4e00-\u9fa5]')  # 中文的编码范围是：\u4e00到\u9fa5
    zh = " ".join(p2.split(line)).strip()
    zh = ",".join(zh.split())
    outStr = zh  # 经过相关处理后得到中文的文本
    return outStr


if __name__ == "__main__":
    # filenames = get_filenames_dir('./raw_data')
    filenames = [config.item_json]
    contents = []
    outfile = open(config.contents,'w')
    for filename in filenames:
        print('dealing with : ' + filename)
        with open(filename,'r') as f:
            line = f.readline()
            while(line):
                dic = json.loads(line)
                for con in dic['content']:
                    content = Reverse_chinese(con)
                    contents.append(content)
                    outfile.write(content)
                line = f.readline()
    outfile.close()



