# -*- coding=utf-8 -*-
from collections import Counter

import jieba
from pymongo import MongoClient

client = MongoClient()  # 默认连接 localhost 27017
db = client.chatlog
post = db.vczh

word_list = []
for doc in post.find({}, {'text': 1}):
    print(len(word_list))
    word_list.extend(jieba.lcut(doc['text'][0]))

word_dict = Counter(word_list)

fp = open('res.txt', 'w', encoding='utf-8')

for key in word_dict:
    fp.write(str(word_dict[key]) + str(key) + '\n')

fp.close()

client.close()
