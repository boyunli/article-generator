# coding=utf-8

from celery import Celery

from python.sites.news.sohu import SoHu
from python.sites.news.toutiao import TouTiao
from python.sites.news.wechat import Wechat


celery_app = Celery('article', include=['python.tasks.workers'])
celery_app.config_from_object('python.tasks.celery_config')

@celery_app.task(bind=True)
def crawler_news(self):
    try:
        SoHu().parse()
        TouTiao().parse()
        Wechat().parse()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=1*60, max_retries=5)

