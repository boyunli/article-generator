import re

def trim(line):
    return re.sub('[\r\s\[\]]', '', line)

