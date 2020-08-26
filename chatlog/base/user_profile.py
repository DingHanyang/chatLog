"""
    构建用户基本画像
    @author:DingHanyang
"""
from datetime import datetime
from pymongo import MongoClient


class UserProfile:
    def __init__(self, db_name='chatlog', collection_name='vczh'):
        print("正在初始化用户画像模块")
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client[db_name]
        self.post = self.db[collection_name]

        self.res_list = [doc for doc in self.post.find({}, {'_id': 0})]

    def close(self):
        self.client.close()

    def _get_user_id_list(self):
        """
        获取记录中所有ID的列表
        :return:[id1,id2,id3,...]
        """
        user_id_list = [li['ID'] for li in self.res_list]

        user_id_list = list(set(user_id_list))
        print('记录中共有', len(user_id_list), '位聚聚发过言')

        return user_id_list

    def _get_all_name(self, user_id):
        """
        根据ID返回一个用户所有曾用名
        :param user_id:用户ID
        :return:{'name1','name2',...}
        """
        name_list = set()
        for li in self.res_list:
            if li['ID'] == user_id:
                name_list.add(li['name'])

        return list(name_list)

    def _get_speak_infos(self, user_id):
        """
        返回一个用户的发言次数,发言文字数,发言图片数
        :param user_id:用户ID
        :return:[speak_num,word_num,photo_num]
        """
        speak_num = 0
        word_num = 0
        photo_num = 0
        for li in self.res_list:
            if li['ID'] == user_id:
                speak_num += 1
                for sp in li['text']:
                    word_num += len(sp)
                    photo_num += sp.count('[图片]')
        return speak_num, word_num, photo_num

    def _get_online_time(self, user_id):
        """
        返回一个用户在那个时段发言数最多(0-24小时)(周1-7)
        :param user_id:用户ID
        :return:[[0,0,0,0],[],[],[],...] [周1-7]包含[0-24小时]
        """
        time_list = []
        for li in self.res_list:
            if li['ID'] == user_id:
                time_list.append(li['time'])

        week_list = [[0 for _ in range(24)] for _ in range(7)]

        for li in time_list:
            week_list[int(datetime.strptime(li, "%Y-%m-%d %H:%M:%S").weekday())][int(li[11:13])] += 1

        return week_list

    def work(self):
        """
        分析所有用户基本画像并存入数据库
        ..note::
            ID:
            name:[name1,name2,...]
            speak_num:发言次数
            word_num:发言字数
            photo_num:发布图片数
            week_online:周活跃分布
        :return:None
        """
        post = self.db.profile
        user_id_list = self._get_user_id_list()
        for li in user_id_list:
            print('正在构建用户', li, '的用户画像')
            name_list = self._get_all_name(li)
            speak_num, word_num, photo_num = self._get_speak_infos(li)
            week_online = self._get_online_time(li)
            ban_time = self._ban_time(li)
            post.insert_one({'ID': li, 'name_list': name_list, 'speak_num': speak_num,
                             'word_num': word_num, 'photo_num': photo_num,
                             'week_online': week_online, 'ban_time': ban_time})
        self.close()

    # TODO 管理员若解禁则扣除时间
    def _ban_time(self, user_id):
        """
        统计用户累计禁言时间
        :return:
        """

        def add_time(add_list):
            time = 0
            for times in add_list:
                for info in [('天', 60 * 24), ('小时', 60), ('分钟', 1)]:
                    if info[0] in times:
                        index = times.find(info[0])
                        if times[index - 2].isdigit():
                            time += int(times[index - 2:index]) * info[1]
                        else:
                            time += int(times[index - 1:index]) * info[1]
            return time

        name_list = self._get_all_name(user_id)
        res_list = []
        for li in self.post.find({'ID': '10000'}, {'text': 1}):
            if '被管理员禁言' in li['text'][0]:
                res_list.append(li['text'][0].split(' 被管理员禁言'))

        time_list = []
        for li in res_list:
            for name in name_list:
                if li[0] == name:
                    time_list.append(li[1])

        return add_time(time_list)
