# -*- coding=utf-8 -*-
'''
    对导出的聊天记录进行数据清洗
    @author:DingHanyang
'''

from pymongo import MongoClient
import re

# 初始化两个常用正则
time_pattern = re.compile(
    r"^(((20[0-3][0-9]-(0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|"
    r"(20[0-3][0-9]-(0[2469]|11)-(0[1-9]|[12][0-9]|30))) (20|21|22|23|[0-9]|[0-1][0-9]):[0-5][0-9]:[0-5][0-9])")
ID_pattern = re.compile(
    r"[(][1-9]\d{4,}[)]$|[<][A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}[>]$")

def judge(str):
    '''
    判断某行是不是起始行
    条件1:YYYY-MM-DD HH-MM-SS开头(长度大于19)
    条件2::(XXXXXXXXX)或者<xxx@xxx.xxx>结尾
    :param str:一行记录
    :return: None or (time,ID)
    '''
    if len(str) > 19 and (time_pattern.match(str)) and (ID_pattern.search(str)):
        return time_pattern.search(str).group(), ID_pattern.search(str).group()

def work():

    '''
    腾讯导出的聊天记录是UTF-8+bom的 手动改成 -bom
    进行数据清洗,将原始数据划分成块保存进mongodb中
    ..note::例子
        time:YYYY-MM-DD HH-MM-SS
        ID:(XXXXXXXXX)或者<xxx@xxx.xxx>
        name:username
        text:['sentence1','sentence2',...]
    '''

    client = MongoClient()  # 默认连接 localhost 27017
    db = client.chatlog
    post = db.vczh

    fp = open('../chatlog.txt', 'r', encoding='utf-8')
    chatlog_list = []
    for line in fp.readlines():
        if line.strip() != "":
            chatlog_list.append(line.strip())
    fp.close()

    print(len(chatlog_list))
    pos = 0 # 当前分析位置
    last =0 # 上一个行首位置
    flag = 0
    id = 0 #mongodb中自行编号_id

    while pos < len(chatlog_list):
        if judge(str(chatlog_list[pos])):
            if flag == 0:
                tup = judge(str(chatlog_list[pos]))
                last = pos
                flag = 1
            else:
                flag = 0
                time = tup[0]
                ID = tup[1]
                # 如果什么消息都没发直接不插入
                if chatlog_list[last + 1:pos]==[]:
                    continue

                for i in '()<>':
                    ID = ID.replace(i, "")
                name = chatlog_list[last].replace(tup[1], "").replace(tup[0],"").lstrip()

                # 为什么会有人取名叫   【狗】【熊】吉！！！！！
                # 由于等级标签有极大部分缺失，所以直接去除
                for i in ['【一见倾心】','【风华绝代】','【富甲一方】','【超凡脱俗】','【蛆】','【渣】',
                          '【狗】','【鹅】','【熊】','【毛子】','【管理员】','【群主】','【仓鼠】']:
                    if name[:len(i)] == i:
                        name=name.replace(i,"")

                # 将时间格式统一
                for li in '0123456789':
                    time = time.replace(' ' + li + ':', ' 0' + li + ':')

                post.insert_one({'_id': id, 'time': time, 'ID': ID, 'name': name,
                                 'text': chatlog_list[last + 1:pos]})
                id += 1
                print('time:', time, "ID:", ID, 'name:', name)
                print(chatlog_list[last + 1:pos])
                print("------------------------------------------------")
                continue
        pos += 1
    client.close()

if __name__ == '__main__':
    print('进行数据清洗')
    work()
    print('数据清洗完成')