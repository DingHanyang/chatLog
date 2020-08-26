"""
    总体数据统计分析
    @author:DingHanyang
"""
import numpy
from pymongo import MongoClient


class Collectivity(object):
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.vczh

    def get_all_speak_info(self):
        """
        群总体在线时间分布
        :return:
        """
        post = self.db.profile
        week_online = numpy.zeros((7, 24), dtype=numpy.int)
        for doc in post.find({}, {'week_online': 1}):
            week_online += numpy.array(doc['week_online'])

        return week_online.tolist()

    def close(self):
        self.client.close()
