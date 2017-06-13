# -*- coding=utf-8 -*-
'''
    构建用户基本画像
    @author:DingHanyang
'''
from pymongo import MongoClient
from datetime import datetime

class userProfile():
    def __init__(self):
        print("正在初始化用户画像构建模块")
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.vczh

        self.res_list = []
        # 读出所有数据
        for doc in self.post.find({}, {'_id': 0}):
            self.res_list.append(doc)

    def close(self):
        self.client.close()

    def get_ID_list(self):
        '''
        获取记录中所有ID的列表
        :return:[id1,id2,id3,...]
        '''
        ID_list = []
        for li in self.res_list:
            ID_list.append(li['ID'])

        ID_list = list(set(ID_list))
        print('记录中共有', len(ID_list), '位聚聚发过言')

        return ID_list

    def get_all_name(self, ID):
        '''
        根据ID返回一个用户所有曾用名
        :param ID:用户ID
        :return:{'name1','name2',...}
        '''
        name_list = set()
        for li in self.res_list:
            if li['ID'] == ID:
                name_list.add(li['name'])

        return list(name_list)

    def get_speak_infos(self, ID):
        """
        返回一个用户的发言次数,发言文字数,发言图片数
        :param ID:用户ID
        :return:[speak_num,word_num,photo_num]
        """
        speak_num = 0
        word_num = 0
        photo_num = 0
        for li in self.res_list:
            if li['ID'] == ID:
                speak_num += 1
                for sp in li['text']:
                    word_num += len(sp)
                    photo_num += sp.count('[图片]')
        return speak_num, word_num, photo_num

    def get_online_time(self, ID):
        """
        返回一个用户在那个时段发言数最多(0-24小时)
        :param ID:用户ID
        :return:[nums,nums,nums,...,nums] 下标0-23表示时间 [nums,nums,...,nums] 下标1-7表示周一到周日
        """
        time_list = []
        for li in self.res_list:
            if li['ID'] == ID:
                time_list.append(li['time'])

        week = [0 for i in range(7)]
        day = [0 for i in range(24)]

        for li in time_list:
            week[int(datetime.strptime(li, "%Y-%m-%d %H:%M:%S").weekday())] += 1
            day[int(li[11:13])] += 1

        return week, day

    def analyse_all_profile(self):
        """
        分析所有用户基本画像并存入数据库
        ..note::
            ID:
            name:[name1,name2,...]
            speak_num:发言次数
            word_num:发言字数
            photo_num:发布图片数
            week_online:周活跃分布
            day_online:日活跃分布
        :return:None
        """
        post=self.db.profile
        ID_list=self.get_ID_list()
        for li in ID_list:
            print('正在构建用户',li,'的用户画像')
            name_list=self.get_all_name(li)
            speak_num,word_num,photo_num=self.get_speak_infos(li)
            week_online,day_online=self.get_online_time(li)
            ban_time=self.ban_time(li)
            dict={'ID':li,'name_list':name_list,'speak_num':speak_num,
                  'word_num':word_num,'photo_num':photo_num,
                  'week_online':week_online,'day_online':day_online,'ban_time':ban_time}
            post.insert_one(dict)

    #TODO 管理员若解禁则扣除时间
    def ban_time(self,ID):
        '''
        统计用户累计禁言时间
        :return:
        '''
        name_list=self.get_all_name(ID)
        res_list = []
        for li in self.post.find({'ID': '10000'}, {'text': 1}):
            if '被管理员禁言' in li['text'][0]:
                res_list.append(li['text'][0].split(' 被管理员禁言'))

        def add_time(time_list):
            time = 0
            for li in time_list:
                if '分钟' in li:
                    time += int(li[:-2])
                elif '小时' in li:
                    time += int(li[:-2]) * 60
                elif '天' in li:
                    time += int(li[:-1]) * 60 * 24
            return time

        time_list=[]
        for li in res_list:
            for name in name_list:
                if li[0] == name:
                    time_list.append(li[1])

        return add_time(time_list)




if __name__ == '__main__':
    userProfile = userProfile()
    userProfile.analyse_all_profile()
    userProfile.close()
