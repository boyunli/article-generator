import re

def trim(line):
    return re.sub('[\r\s\[\]]', '', line)

def filter_(content):
    '''
    过滤违禁词
    '''
    #match = re.match(r'.*(雪茄|烟|酒|私服).*', content)
    #return True if match else False
    return re.sub('[雪茄|烟|酒|私服|药|荡妇|热气球|第一夫人|糖尿病|军c|共产党]', '*', content)
