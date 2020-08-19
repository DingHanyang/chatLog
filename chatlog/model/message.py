from mongoengine import *


class Message(Document):
    meta = {'db_alias': 'chatlog'}

    name = StringField()  # 发言用户昵称
    ID = StringField()  # 发言用户ID
    time = DateTimeField()  # 该消息发送时间
    text = ListField()  # 发送消息的列表
