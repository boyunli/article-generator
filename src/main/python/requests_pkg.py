# -*- coding:utf-8 -*-

import os
import time
import json
import random

import requests
from selenium import webdriver
from fake_useragent import UserAgent
from fake_useragent.errors import FakeUserAgentError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _crawl_proxy_ip():
    resp = requests.get('http://ubuntu.pydream.com:8000/?types=0&count=5&country=国内')
    socks = json.loads(resp.text)
    sock = random.choice(socks)
    return (sock[0], sock[1])

def get_rotate_headers(referer=None):
    ua = get_ua()
    headers = {
            "User-Agent": ua,
            "Referer" : referer if referer else None,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            # "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            }
    return headers

def get_ua():
    ua = ''
    try:
        ua = UserAgent().random
    except FakeUserAgentError:
        file = os.path.join(BASE_DIR, 'user_agent.txt')
        with open(file, 'r') as f:
            uas = f.readlines()
            ua = random.choice(uas).strip()
    print('UserAgent: {}'.format(ua))
    return ua

def get_chrome_options(host=None, origin=None, referer=None, proxy=False):
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    options.add_argument('headless')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('user-agent={}'.format(get_ua()))
    # options.add_argument('--start-maximized')
    options.add_argument('window-size=1920x1080')
    if host:
        options.add_argument('host={}'.format(host))
    if referer:
        options.add_argument('referer={}'.format(referer))
    if origin:
        options.add_argument('origin={}'.format(origin))
    # 设置不加载图片
    options.add_experimental_option("prefs", prefs)
    if proxy:
        host, port = _crawl_proxy_ip()
        options.add_argument('--proxy-server={}:{}'.format(host, port))
    return options

# 配置 PhantomJS
def phantomjs_args():
    host, port = _crawl_proxy_ip()
    return [
        "--load-images=no",
        "--disk-cache=yes",
        "--ignore-ssl-errors=true",
        "--proxy-type=http",
        "--proxy=%(host)s:%(port)s" % {
                    "host": host,
                    "port": port
                }
    ]

def set_proxies():
    host, port = _crawl_proxy_ip()
    config = {
        "http": "http://{host}:{port}".format(host=host, port=port),
    }
    return host, config

def delete_no_use_proxy_ip(ip):
    requests.get('http://ubuntu.pydream.com:8000/delete?ip={ip}'.format(ip=ip))


def request_get(url, cookies=None, referer=None, timeout=(3.05, 10)):
    retry_count = 0
    ip = ''
    while True:
        try:
            ip, proxies = set_proxies()
            if all([cookies, referer]):
                res = requests.get(url, cookies=cookies,
                                   headers=get_rotate_headers(referer=referer),
                                   proxies=proxies, timeout=15,  verify=False)
            else:
                res = requests.get(url, headers=get_rotate_headers(),
                                   proxies=proxies, timeout=15,  verify=False)
            return res
        except requests.exceptions.ProxyError:
            print('{flag} 代理无效 {flag}'.format(flag='-'*30))
            delete_no_use_proxy_ip(ip)
            retry_count += 1
            time.sleep(1)
            if retry_count == 5:
                return False
        except Exception:
            time.sleep(1)
            retry_count += 1
            if retry_count == 5:
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



