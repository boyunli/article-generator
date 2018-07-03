#!/bin/sh

cd ~/py3/article-generator/src/main
source /usr/bin/virtualenvwrapper.sh
workon article_generator
python python/sites/news/toutiao.py
python python/sites/news/sohu.py
python python/sites/news/wechat.py
