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
    资讯详情
    '''
    category = CharField(verbose_name='类别', max_length=10)  # 手表、包包
    site = CharField(verbose_name='站点', max_length=20)
    tag = CharField(verbose_name='标签', max_length=100)
    title = CharField(verbose_name='标题', max_length=300)
    content = TextField(verbose_name='content')
    author = CharField(verbose_name='作者', max_length=50)
    news_url = CharField(max_length=200, verbose_name='资讯URL')
    publish_time = CharField(verbose_name='发布时间', max_length=50)

    class Meta:
        db_table = 'news'


