# -*- coding:utf-8 -*-

from peewee import Model,\
    CharField, TextField
from playhouse.db_url import connect

from python.settings import URL

class BaseModel(Model):
    class Meta:
        database = connect(URL)

class News(BaseModel):
    '''
    手表资讯详情
    '''
    site = CharField(verbose_name='站点', max_length=20)
    tag = CharField(verbose_name='标签', max_length=100)
    title = CharField(verbose_name='标题', max_length=300)
    first = TextField(verbose_name='开头')
    second = TextField(verbose_name='中间')
    third = TextField(verbose_name='结尾')
    author = CharField(verbose_name='作者', max_length=50)
    news_url = CharField(max_length=200, verbose_name='资讯URL')
    publish_time = CharField(verbose_name='发布时间', max_length=50)

    class Meta:
        db_table = 'watch_news'


