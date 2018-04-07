# -*- coding:utf-8 -*-

import datetime

from peewee import Model,\
    CharField, DateTimeField, \
    ForeignKeyField, TextField
from playhouse.db_url import connect

from python.settings import URL

class BaseModel(Model):
    class Meta:
        database = connect(URL)


class NewsSite(BaseModel):
    '''
    资讯站点
    '''
    site = CharField(verbose_name='站点',max_length=20)
    tag = CharField(verbose_name='标签', max_length=30, default='-1')
    news_url = CharField(unique=True, max_length=200, verbose_name='资讯URL')

    class Meta:
        db_table = 'watch_news_site'
        indexes = (
            (('site', 'tag'), True),
        )


class News(BaseModel):
    '''
    手表资讯详情
    '''
    site = ForeignKeyField(NewsSite, related_name='news')
    title = CharField(verbose_name='标题', max_length=300)
    first = TextField(verbose_name='开头')
    second = TextField(verbose_name='中间')
    third = TextField(verbose_name='结尾')
    author = CharField(verbose_name='作者', max_length=50)
    publish_time = DateTimeField(verbose_name='发布时间',
                                default=datetime.datetime.today)

    class Meta:
        db_table = 'watch_news'


