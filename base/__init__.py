from .CutWord import cutword
from .DataClean import dataclean
from .UserProfile import userProfile


def work():
    clean = dataclean()
    clean.work()
    profile = userProfile()
    profile.work()
    cut = cutword()
    cut.work()
