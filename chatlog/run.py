from analysis.collectivity import Collectivity
from analysis.individual import Individual
from analysis.interesting import Interesting
from base.read_chatlog import ReadChatlog
from base.user_profile import UserProfile
from datetime import datetime

if __name__ == '__main__':
    RC = ReadChatlog('./chatlog.txt')
    RC.work()  # 进行聊天记录的清洗并入库
    UP = UserProfile()
    UP.work()  # 构建简单的用户画像

    # Collectivity
    # col = Collectivity()
    # print(col.get_all_speak_info())  # 群聊天时间分布

    # Individual
    # ind = Individual()
    # print(ind.longest_ban())  # 禁言时长的排名
    # print(ind.most_speak('speak_num'))  # 发言次数的排名

    # Interesting
    # interest = Interesting()
    # print(interest.longest_formation())  # 最长队形的排名
    # print(interest.longest_name())  #  最长的马甲排名
