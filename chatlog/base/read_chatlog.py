import re

from pymongo import MongoClient

from chatlog.base import constant


class ReadChatlog(object):
    def __init__(self, file_path, db_name='chatlog', collection_name='vczh'):
        self.file_path = file_path
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client[db_name]
        self.post = self.db[collection_name]

        # 初始化两个常用正则
        self.time_pattern = re.compile(constant.JUDGE_TIME_RE)
        self.ID_pattern = re.compile(constant.JUDGE_ID_RE)

    def judge_start_line(self, message):
        """
        判断某行是不是起始行
        条件1:YYYY-MM-DD HH-MM-SS开头(长度大于19)
        条件2::(XXXXXXXXX)或者<xxx@xxx.xxx>结尾
        :return: False or (time,ID)
        """
        if len(message) > 19 and (self.time_pattern.match(message)) and (self.ID_pattern.search(message)):
            return self.time_pattern.search(message).group(), self.ID_pattern.search(message).group()
        return False

    def work(self):
        """
        腾讯导出的聊天记录是UTF-8+bom的 手动改成-bom
        进行数据清洗,将原始数据划分成块保存进mongodb中
        ..note::例子
            time:YYYY-MM-DD HH-MM-SS
            ID:(XXXXXXXXX)或者<xxx@xxx.xxx>
            name:username
            text:['sentence1','sentence2',...]
        """
        print('----------正在进行数据清洗-------------')

        with open(self.file_path, 'r', encoding='utf-8') as chatlog_file:
            chatlog_list = [line.strip() for line in chatlog_file if line.strip() != ""]

        now_cursor = 0  # 当前分析位置
        last = 0  # 上一个行首位置
        flag = 0
        first_line_info = self.judge_start_line(str(chatlog_list[now_cursor]))
        while now_cursor < len(chatlog_list):
            if self.judge_start_line(str(chatlog_list[now_cursor])):
                if not flag:
                    first_line_info = self.judge_start_line(str(chatlog_list[now_cursor]))
                    last = now_cursor
                    flag = 1
                else:
                    flag = 0
                    send_time = first_line_info[0]
                    send_id = first_line_info[1]
                    # 如果什么消息都没发直接不插入
                    if not chatlog_list[last + 1:now_cursor]:
                        continue
                    # 发送该消息时用户的马甲
                    name = chatlog_list[last].replace(send_id, "").replace(send_time, "").lstrip()

                    for extra_char in '()<>':
                        send_id = send_id.replace(extra_char, "")

                    # 由于等级标签有极大部分缺失，所以直接去除
                    # TODO:消息中大频率出现的标签应该就是等级标签，应自检测
                    for i in ['【实习】', '【能写代码】', '【专属骚头衔】', '【群地位倒数】', '【实习】', '【管理员】']:
                        if name[:len(i)] == i:
                            name = name.replace(i, "")

                    # 将时间格式统一
                    for li in '0123456789':
                        send_time = send_time.replace(' ' + li + ':', ' 0' + li + ':')

                    self.post.insert_one({'time': send_time, 'ID': send_id, 'name': name,
                                          'text': chatlog_list[last + 1:now_cursor]})

                    print('time:', send_time, 'ID:', send_id, 'name:', name)
                    print(chatlog_list[last + 1:now_cursor])
                    print("------------------------------------------------")
                    continue
            now_cursor += 1
        self.client.close()
        print('----------数据清洗完成-------------')

