# -*- coding=utf-8 -*-
'''
    总体数据统计分析
    @author:DingHanyang
'''
from pymongo import MongoClient


class collecticity:
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.vczh

    def get_all_speak_info(self):
        '''
        群总体在线时间分布
        :return:
        '''
        post = self.db.profile
        week_online = [0 for i in range(7)]
        day_online = [0 for i in range(24)]
        for doc in post.find({}, {'day_online': 1, 'week_online': 1}):
            week_online = [i + j for i, j in zip(week_online, doc['week_online'])]
            day_online = [i + j for i, j in zip(day_online, doc['day_online'])]

        return week_online,day_online

    def close(self):
        self.client.close()

if __name__ == '__main__':
    col=collecticity()
    print(col.get_all_speak_info())
    col.close()