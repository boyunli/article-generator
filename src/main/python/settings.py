# coding:utf-8

import os
import logging
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'cgll.123'
MYSQL_DB = 'price_system'
URL = 'mysql+pool://{user}:{passwd}@{host}:{port}/{db}?charset=utf8mb4&max_connections=20&stale_timeout=300'\
    .format(user=MYSQL_USER, passwd=MYSQL_PASSWD,
            host=MYSQL_HOST, port=3306, db=MYSQL_DB)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(pathname)s:%(lineno)d][%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}
    },
    #过滤器，表明一个日志信息是否要被过滤掉而不记录
    'filters': {
    },
    #处理器
    'handlers': {
        'spider': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/spider.log',
            'maxBytes': 1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
        },
        'spider_error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/spider_error.log',
            'maxBytes':1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
			        },
        'data': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':BASE_DIR + '/log/data.log',
            'maxBytes': 1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'data_error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/data_error.log',
            'maxBytes':1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'web': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':BASE_DIR + '/log/web.log',
            'maxBytes': 1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'web_error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/web_error.log',
            'maxBytes':1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
        'task': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':BASE_DIR + '/log/task.log',
            'maxBytes': 1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
			 },
        'task_error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR + '/log/task_error.log',
            'maxBytes':1024*1024*5,
            # 'backupCount': 5,
            'formatter':'standard',
            },
    },
    # 记录器
    'loggers': {
        'data': {
            'handlers': ['console', 'data', 'data_error'],
            'level': 'DEBUG',  #级别最低
            'propagate': False
        },
        'spider': {
            'handlers': ['console', 'spider', 'spider_error'],
            'level': 'DEBUG',
            'propagate': False
        },
        'web': {
            'handlers': ['console', 'web', 'web_error'],
            'level': 'DEBUG',
            'propagate': False
        },
        'task': {
            'handlers': ['console', 'task', 'task_error'],
            'level': 'DEBUG',
            'propagate': False
        },
    }

}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('spider')
dblogger = logging.getLogger('data')
weblogger = logging.getLogger('web')
tasklogger = logging.getLogger('task')
