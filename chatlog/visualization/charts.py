# -*- coding=utf-8 -*-
"""
    数据可视化模块
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pymongo import MongoClient

from chatlog.analysis.individual import Individual


class Charts(object):
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.profile

    def ban_time(self):
        ind = Individual()
        res_list = ind.longest_ban()
        res_list = res_list[0:10]
        print(res_list)
        name_list = [i[1] for i in res_list]
        time_list = [i[2] for i in res_list]

        sns.set(style="darkgrid")
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        f, ax = plt.subplots(figsize=(18.5, 9))

        # Plot the crashes where alcohol was involved
        sns.set_color_codes("muted")
        sns.barplot(x=time_list, y=name_list,
                    label="禁言时长", color="y")

        # Add a legend and informative axis label
        ax.legend(ncol=2, loc="lower right", frameon=True)
        ax.set(xlim=(0, time_list[0]), ylabel="",
               xlabel="禁言时间最长")
        sns.despine(left=True, bottom=True)

        plt.savefig('../photos/ban_time.png', format='png', dpi=400)
        plt.close()

    def speak_photo_in_total(self):
        """
        发言次数前10的用户及发送图片的比例
        :return:
        """
        ind = Individual()
        res_list = ind.most_speak('speak_num')
        res_list = res_list[0:10]
        print(res_list)
        ID_list = [i[0] for i in res_list]
        name_list = [i[1] for i in res_list]
        speak_list = [i[2] for i in res_list]
        photo_num = []
        for id in ID_list:
            for doc in self.post.find({'ID': id}, {'photo_num': 1}):
                photo_num.append(doc['photo_num'])
        sns.set(style="darkgrid")
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        f, ax = plt.subplots(figsize=(18.5, 9))

        sns.set_color_codes("pastel")
        sns.barplot(x=speak_list, y=name_list,
                    label="发言次数", color="b")

        # Plot the crashes where alcohol was involved
        sns.set_color_codes("muted")
        sns.barplot(x=photo_num, y=name_list,
                    label="发送图片数", color="b")

        # Add a legend and informative axis label
        ax.legend(ncol=2, loc="lower right", frameon=True)
        ax.set(xlim=(0, speak_list[0]), ylabel="",
               xlabel="群里发言次数排行及发送图片的比例")
        sns.despine(left=True, bottom=True)

        plt.savefig('../photos/speak_photo_in_total.png', format='png', dpi=300)
        plt.close()

    def user_online_time(self, user_ID=None):
        """
        绘制(全体)用户活跃时间图像
        :param user_ID:默认为空,指定全体用户,不为空时为指定ID用户
        """
        res_list = []
        if user_ID:
            find_dict = {'ID': user_ID}
        else:
            find_dict = {}

        week_online = [[0 for _ in range(24)] for _ in range(7)]
        for doc in self.post.find(find_dict, {'week_online': 1}):
            for i in range(0, 7):
                for j in range(0, 24):
                    if user_ID:
                        week_online[i][j] = doc['week_online'][i][j]
                    else:
                        week_online[i][j] += doc['week_online'][i][j]

        week_online = np.array([li for li in week_online])
        columns = [str(i) + '-' + str(i + 1) for i in range(0, 24)]
        index = ['Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.']

        week_online = pd.DataFrame(week_online, index=index, columns=columns)
        plt.figure(figsize=(18.5, 9))
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
        sns.set()

        # Draw a heatmap with the numeric values in each cell
        sns.heatmap(week_online, annot=True, fmt="d", cmap="YlGnBu")
        plt.savefig('../photos/user_time_online.png', format='png', dpi=300)
        plt.close()

    def close(self):
        self.client.close()

    def work(self):
        self.speak_photo_in_total()
        self.user_online_time()
        self.close()


if __name__ == '__main__':
    chart = Charts()
    chart.user_online_time()
