"""
    聊天内容分析
    @author:DingHanyang
"""
from pymongo import MongoClient


class ChatText(object):
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.vczh

        # TODO:一个大坑未填
