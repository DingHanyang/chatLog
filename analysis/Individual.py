# -*- coding=utf-8 -*-
'''
    个体数据统计分析
    @author:DingHanyang
'''
from pymongo import MongoClient


class individual:
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.profile

    def most_speak(self,type):
        '''
        发言次数最多、发送字数最多、发送图片最多的用户排行
        :param type:选择 word_num,speak_num,photo_num
        :return:[(ID1,name1,num),(ID1,name2,num),...]
        '''
        top_list=[]
        for doc in self.post.find({},{type:1,'name_list':1,'ID':1}):
            top_list.append((doc['ID'],doc['name_list'][len(doc['name_list'])-1],doc[type]))

        top_list = sorted(top_list, key=lambda x: x[2], reverse=True)  # 从大到小排序

        # for li in top_list:
        #     print(li[0], li[1],li[2])

        return top_list

    def longest_ban(self):
        '''
        被禁言时间最长的人榜单
        :return:[(name1,time),(name2,time),...]
        '''
        self.post=self.db.profile
        top_list = []
        for doc in self.post.find({}, {'ID':1,'ban_time': 1,'name_list':1}):
            top_list.append((doc['ID'],doc['name_list'][len(doc['name_list'])-1],doc['ban_time']))

        top_list = sorted(top_list, key=lambda x: x[2], reverse=True)  # 从大到小排序
        for li in top_list:
            print(li[0], li[1],li[2])

        return top_list




    def close(self):
        self.client.close()


if __name__ == '__main__':
    individual=individual()
    individual.longest_ban()
    individual.close()
