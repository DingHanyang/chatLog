from chatlog.analysis.collectivity import Collectivity
from chatlog.analysis.individual import Individual
from chatlog.analysis.interesting import Interesting
from chatlog.base.read_chatlog import ReadChatlog
from chatlog.base.user_profile import UserProfile

if __name__ == '__main__':
    RC = ReadChatlog('./group1.txt')
    RC.work()
    UP = UserProfile()
    UP.work()

    # Collectivity
    # col = Collectivity()
    # print(col.get_all_speak_info())  # 群聊天时间分布

    # Individual
    # ind = Individual()
    # print(ind.longest_ban())
    # print(ind.most_speak('speak_num'))

    # Interesting
    # interest = Interesting()
    # print(interest.longest_formation())
    # print(interest.longest_name())
