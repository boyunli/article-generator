import os
import re

import jieba

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def segment(article):
    jieba.load_userdict('{}/brands.txt'.format(BASE_DIR))
    seg_list = jieba.cut(article)
    result = ' '.join(seg_list)
    return re.sub('[0-9.。:：,，)）(（！!??”“\"]', '', result).split()
