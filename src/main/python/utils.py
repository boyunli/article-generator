import re

def trim(line):
    return re.sub('[\r\s\[\]]', '', line)

def filter_(content):
    '''
    过滤违禁词
    '''
    match = re.match(r'.*(雪茄|烟|酒).*', content)
    return True if match else False
