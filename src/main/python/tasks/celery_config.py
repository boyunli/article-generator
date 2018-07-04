# coding=utf-8
from kombu import Queue
from kombu import Exchange
from celery.schedules import crontab

from datetime import timedelta

BROKER_URL = 'redis://:helloworld@0.0.0.0:6379/13'  # 指定 Broker

CELERY_RESULT_BACKEND = 'redis://:helloworld@0.0.0.0:6379/15'  # 指定 Backend

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERY_ENABLE_UTC = True

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化 ls: json yaml msgpack pickle(不推荐)

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 4  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_IMPORTS = (  # 指定导入的任务模块
    'python.tasks.workers',
)

CELERY_TASK_PUBLISH_RETRY = False  # 重试

# schedules
CELERYBEAT_SCHEDULE = {
    'crawler_news': {
        'task': 'python.tasks.workers.crawler_news',
        # 9,14,23
        # 'schedule': crontab(hour='1,6,15,9', minute='09'),
        'schedule': timedelta(minutes=60),
        'options': {'queue': 'crawler_news',
                    'routing_key': 'for_crawler_news'}
    },
}

CELERY_QUEUES = (
    Queue('crawler_news', Exchange('crawler_news'),
          type='direct', routing_key='for_crawler_news'),
)

CELERY_ROUTES = {
    'crawler_news': {'queue': 'crawler_news', 'routing_key': 'for_crawler_news'},
}
