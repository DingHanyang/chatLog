# -*- coding=utf-8 -*-
'''
    总体数据统计分析
    @author:DingHanyang
'''
from pymongo import MongoClient


class collecticity:
    def __init__(self):
        client = MongoClient()  # 默认连接 localhost 27017
        db = client.chatlog
        post = db.vczh
