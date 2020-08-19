from mongoengine import *


class User(Document):
    meta = {'db_alias': 'chatlog'}

    name_now = StringField()  # 用户当前昵称
    name_list = ListField(StringField)  # 用户历史昵称列表
    ID = StringField()  # ID用户ID
    speak_num = IntField()  # 用户发言次数
    word_num = IntField()  # 用户发送文本分词后的词数
    photo_num = IntField()  # 用户发送图片的数量
    ban_num = IntField()  # 用户被禁言的次数
    ban_time_sum = DateTimeField()  # 用户被禁言时间总和
