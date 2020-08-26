"""
    个体数据统计分析
    @author:DingHanyang
"""
from pymongo import MongoClient


class Individual(object):
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.profile

    def most_speak(self, send_class='speak_num'):
        """
        发言次数最多、发送字数最多、发送图片最多的用户排行
        :param send_class:选择 speak_num,word_num,photo_num
        :return:[(ID1,name1,num),(ID1,name2,num),...]
        """
        top_list = []
        for doc in self.post.find({}, {send_class: 1, 'name_list': 1, 'ID': 1}):
            top_list.append((doc['ID'], doc['name_list'][len(doc['name_list']) - 1], doc[send_class]))

        return sorted(top_list, key=lambda x: x[2], reverse=True)

    def longest_ban(self):
        """
        被禁言时间最长的人榜单
        :return:[(name1,time),(name2,time),...]
        """
        self.post = self.db.profile
        top_list = []
        for doc in self.post.find({}, {'ID': 1, 'ban_time': 1, 'name_list': 1}):
            top_list.append((doc['ID'], doc['name_list'][len(doc['name_list']) - 1], doc['ban_time']))

        return sorted(top_list, key=lambda x: x[2], reverse=True)

    def close(self):
        self.client.close()
