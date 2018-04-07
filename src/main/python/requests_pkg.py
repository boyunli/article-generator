# -*- coding:utf-8 -*-

import os

import requests
from fake_useragent import UserAgent
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROXYUSER = "H1IF096FYI74C29D"
PROXYPASS = "10F8046B21581DBA"
PROXYHOST = "proxy.abuyun.com"
PROXYPORT = "9020"

def get_rotate_headers(referer=None):

    #REFERER_LIST = [
    #    'https://www.google.com/',
    #    'https://www.baidu.com/',
    #]
    headers = {
            "User-Agent": UserAgent().random,
            "Referer" : referer if referer else None,   #random.choice(REFERER_LIST),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            # "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
    return headers

# 配置 PhantomJS
SERVICE_ARGS = [
    "--load-images=no",
    "--disk-cache=yes",
    "--ignore-ssl-errors=true",
    "--proxy-type=http",
    "--proxy=%(host)s:%(port)s" % {
        "host": PROXYHOST,
        "port": PROXYPORT,
    },
    "--proxy-auth=%(user)s:%(pass)s" % {
        "user": PROXYUSER,
        "pass": PROXYPASS,
    },
]
DCAP = dict(DesiredCapabilities.PHANTOMJS)
DCAP["phantomjs.page.settings.userAgent"] = UserAgent().random

def set_proxies():
    proxyAuth = PROXYUSER + ":" + PROXYPASS
    proxies = {
            "http": "http://{proxyAuth}@proxy.abuyun.com:9020".format(proxyAuth=proxyAuth)
            }
    return proxies

def request_get(url, cookies=None, referer=None, timeout=(3.05, 10)):
    retry_count = 0
    while True:
        try:
            if not cookies:
                res = requests.get(url, headers=get_rotate_headers(referer=referer),
                                proxies=set_proxies(), timeout=15,  verify=False)
            else:
                res = requests.get(url, cookies=cookies, headers=get_rotate_headers(referer=referer),
                                proxies=set_proxies(), timeout=15,  verify=False)
            return res
        except Exception:
            retry_count += 1
            if retry_count == 3:
                return False

#def new_driver():
#    dcap = dict(DesiredCapabilities.PHANTOMJS)
#    dcap["phantomjs.page.settings.userAgent"] = UserAgent().random
#    driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=SERVICE_ARGS,
#                                 service_log_path=os.path.join(BASE_DIR, 'log/ghostdriver.log'))
#    driver.maximize_window()
#    driver.implicitly_wait(5)
#    driver.set_page_load_timeout(15)
#    return driver
#
#ndriver = new_driver()


