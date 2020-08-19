from .Charts import charts
from .Wordcloud import wordcloud


def work():
    chart = charts()
    word = wordcloud()
    chart.work()
    word.work()
