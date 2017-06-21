# -*- coding=utf-8 -*-
from collections import Counter

import jieba
from pymongo import MongoClient


class cutword():
    def __init__(self):
        self.client = MongoClient()  # 默认连接 localhost 27017
        self.db = self.client.chatlog
        self.post = self.db.vczh

    def work(self):
        stopword_list=[]
        fp = open('../base/chinese_stopword.txt', 'r', encoding='utf-8')
        for line in fp.readlines():
            stopword_list.append(line.replace('\n',''))
        fp.close()

        word_list = []
        for doc in self.post.find({}, {'text': 1}):
            print(len(word_list))
            word_list.extend(jieba.lcut(doc['text'][0]))
        word_dict = Counter(word_list)
        self.post = self.db.word
        for key in word_dict.keys():
            if str(key) in stopword_list:
                print(key)
                continue
            self.post.insert({'word':key,'item':word_dict[key]})
        self.close()

    def close(self):
        self.client.close()


if __name__ == '__main__':
    cut =cutword()
    cut.work()
    cut.close()
