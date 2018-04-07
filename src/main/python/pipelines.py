# -*- coding:utf-8 -*-

from python.models import NewsSite, News
from python.settings import dblogger

def before_request_handler():
    if not NewsSite.table_exists():
        NewsSite.create_table()
    if not News.table_exists():
        News.create_table()

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class NewsPipeline():

    def __init__(self):
        before_request_handler()

    def save(self, watchs):
        for item in watchs:
            dblogger.debug('\033[94m 开始保存文章详细信息:{} \033[0m'\
                        .format(item))
            site = item['site']
            tag = item['tag']
            news_url = item['news_url']

            title = item['title']
            first = item['first']
            second = item['second']
            third = item['third']
            author = item['author']
            publish_time = item['publish_time']

            try:
                site, created = NewsSite.get_or_create(
                    site=site,
                    tag=tag,
                    defaults={
                        'news_url': news_url,
                    })
                if not created:
                    site.news_url = news_url
                    site.save()

                news, news_created = News.get_or_create(
                        site = site,
                        title = title,
                        defaults={
                            'first': first,
                            'second': second,
                            'third': third,
                            'author': author,
                            'publish_time': publish_time,
                        }
                    )
                if not news_created:
                    news.first = first
                    news.second = second
                    news.third = third
                    news.author = author
                    news.publish_time = publish_time
                    news.save()
            except Exception as e:
                dblogger.error('\033[92m error:{} \033[0m'.format(e))




