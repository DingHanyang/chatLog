from .CutWord import cutword
from .UserProfile import userProfile
from .read_chatlog import dataclean


def work():
    clean = dataclean()
    clean.work()
    profile = userProfile()
    profile.work()
    cut = cutword()
    cut.work()
