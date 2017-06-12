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

        return name_list

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


if __name__ == '__main__':
    userProfile = userProfile()
    print(userProfile.get_online_time('2767916879'))
    userProfile.close()
