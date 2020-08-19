from .CutWord import cutword
from .UserProfile import userProfile


def work():
    profile = userProfile()
    profile.work()
    cut = cutword()
    cut.work()
