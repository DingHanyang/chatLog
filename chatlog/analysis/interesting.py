"""
    因吹斯听 分析及统计
    @author:DingHanyang
"""
from pymongo import MongoClient
import xlwt
from datetime import datetime
from datetime import timedelta


class Interesting(object):
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.vczh

    def longest_name(self):
        """
        取出所有用户的name,并排序。
        ..note::由于聊天记录时间跨度大,有的聚聚改名频繁,而有些名字由于QQ保存的原因保存成了QQ号而丢失
        :return:top_list[('name',len(name)),(...,...),...] 按长度从大到小排序
        """
        res_list = []
        for doc in self.post.find({}, {'name': 1}):
            res_list.append(doc['name'])
        res_list = {}.fromkeys(res_list).keys()

        top_list = []
        for li in res_list:
            top_list.append((li, len(li)))

        return sorted(top_list, key=lambda x: x[1], reverse=True)

    def longest_formation(self):
        """
        所有记录中,跟队形最长的聊天记录。
        :return:top_list[('text',len(text)),(...,...),...] 按长度从大到小排序
        """
        res_list = []
        for doc in self.post.find({}, {'text': 1}):
            res_list.append(doc['text'])

        top_list = []
        # text 数据存储形式 [[sentences1],[sentences2],...] 队形大多只有一句 所以只考虑text长度为1的
        i = 0
        while i < len(res_list) - 1:
            if res_list[i][0] == '[图片]':
                i += 1
            elif res_list[i][0] == res_list[i + 1][0]:
                pos = i + 1
                while pos < len(res_list) - 1:
                    if res_list[pos][0] == res_list[pos + 1][0]:
                        pos += 1
                    else:
                        if pos - i + 1 > 2:
                            top_list.append((res_list[i][0], pos - i + 1))
                        i = pos + 1
                        break
            else:
                i += 1

        # 例如中间有人插话一句将队形打断的话,整合队形
        k = 0
        while k < len(top_list) - 1:
            if top_list[k][0] == top_list[k + 1][0]:
                top_list.append((top_list[k][0], top_list[k][1] + top_list[k + 1][1]))
                top_list.pop(k - 1)
                top_list.pop(k)
            else:
                k += 1
        return sorted(top_list, key=lambda x: x[1], reverse=True)
    
    def count_images_by_month(self, start_date: datetime, end_date: datetime):
        """
        统计指定时间段内每个用户每月发的图片数量
        :param start_date: 开始日期
        :param end_date: 结束日期
        """
        # 获取所有用户ID和昵称的映射关系
        id_name_map = {}
        for doc in self.post.find().distinct('ID'):
            user_data = self.post.find_one({'ID': doc})
            id_name_map[user_data['ID']] = user_data['name']

        # 获取所有月份
        months = [start_date.strftime('%Y-%m')]
        while start_date < end_date:
            start_date = start_date.replace(day=28) + timedelta(days=4)
            months.append(start_date.strftime('%Y-%m'))

        # 初始化结果字典
        result = {}
        for user_id in id_name_map:
            result[user_id] = {'name': id_name_map[user_id], 'total': 0}

        # 统计每个用户每月的图片次数
        for user_id in result:
            for month in months:
                result[user_id][month] = 0
                
        for doc in self.post.find():
            user_id = doc['ID']
            month = doc['time'][:7]
            photo_num = 0
            # 计算图片数量,由于数据库中只有合计,所以这里重新计算一下
            for sp in doc['text']:
                photo_num += sp.count('[图片]')
            # print(photo_num)
            result[user_id][month] += photo_num
            result[user_id]['total'] += photo_num

        # 将结果保存到Excel
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Image Count')

        # 写入表头
        header = ['QQ', '昵称'] + months + ['合计']
        for i, col in enumerate(header):
            sheet.write(0, i, col)

        # 写入数据
        row = 1
        for user_id in result:
            sheet.write(row, 0, user_id)
            sheet.write(row, 1, result[user_id]['name'])
            col = 2
            for month in months:
                sheet.write(row, col, result[user_id][month])
                col += 1
            sheet.write(row, col, result[user_id]['total'])
            row += 1

        # 保存Excel文件
        workbook.save('image_count.xls')

        print("图片统计结果已保存到 image_count.xls 文件。")

    def close(self):
        self.client.close()
