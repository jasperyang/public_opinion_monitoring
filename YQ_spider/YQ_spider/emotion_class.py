#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_api.mysql import MySQL
import json
from data_api import emotion_setting
import time
import random

class EmotionAnalysis(object):
    def __init__(self,source):
        data = MySQL.execute(emotion_setting.search_dict[source])
        self.contentList = [i[0] for i in data]
        self.source = source

    def post_requests_retry(self,service,try_num,params):
        if try_num ==0:
            return float(2)
        try:
            time.sleep(1)
            res = service.call(emotion_setting.action, params)
            score = json.loads(res)['positive']
            return score
        except Exception as e :
            import traceback
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            try_num -= 1
            print('now it will try to request. There is '+str(try_num)+' times last.')
            time.sleep(random.randint(1, 2))
            self.post_requests_retry(service, try_num, params)


    def tencent_score(self,content):
        from QcloudApi.qcloudapi import QcloudApi
        params = {'content':content}
        service = QcloudApi(emotion_setting.module,emotion_setting.config)
        score = self.post_requests_retry(service=service,try_num=3,params=params)
        return score

    def get_score(self,tableName):
        # snowNLP的识别
        from snownlp import SnowNLP
        contentScoreSnow = [SnowNLP(i).sentiments for i in self.contentList]
        # Tencent的识别
        contentScoreTencent = [self.tencent_score(i) for i in self.contentList]
        librariesSnow = ['snowNLP' for _ in self.contentList]
        librariesTencent = ['Tencent' for _ in self.contentList]
        sourceName = [self.source for _ in self.contentList]
        tupleListSnow = [(a, b, c, d) for a, b, c, d in zip(self.contentList, contentScoreSnow, sourceName, librariesSnow)]
        tupleListTencent = [(a, b, c, d) for a, b, c, d in zip(self.contentList, contentScoreTencent, sourceName, librariesTencent)]
        tupleList = tupleListSnow + tupleListTencent
        MySQL.insert_data(tableName, tupleList)

if __name__ =='__main__':
    """
    sourceList = emotion_setting.search_dict
    for source in sourceList:
        EmotionAnalysis(source).get_score('emotion_analysis')
    """
    EmotionAnalysis('test').get_score('emotion_analysis')
