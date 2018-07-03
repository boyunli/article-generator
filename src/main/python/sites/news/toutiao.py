import time
import re

from lxml import etree
from selenium import webdriver
from urllib.parse import urljoin

from python.requests_pkg import get_chrome_options,\
    request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class TouTiao():
    '''
    每一个小时爬一次
    爬取头条热点新闻
    '''
    def __init__(self):
        self.url = 'https://www.toutiao.com'

    def parse(self):
        url = 'https://www.toutiao.com/ch/news_hot/'
        chrome_options = get_chrome_options()
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        html = etree.HTML(driver.page_source)
        hrefs = html.xpath('//a[@class="link title"]/@href')
        if not hrefs:
            self.parse()
        logger.debug("\033[92m 开始爬取:{} \033[0m".format(url))
        details = []
        for href in hrefs:
            if href.startswith('http'): continue
            time.sleep(1)
            try:
                href = urljoin(self.url, href)
                item = self._extract(href, url)
                if not item: continue
                details.append(item)
            except IndexError:
                # 像这种很可能是网络原因 导致失败，需要将失败的href写入 某个队列中，待重爬
                continue
        NewsPipeline().save(details)

    def _extract(self, href, referer):
        resp = rget(href, referer=referer)
        if not resp: return
        html = etree.HTML(resp.content)
        if not html: return

        title = ''.join(html.xpath('//title/text()'))
        if title:
            title = trim(title)
        else:
            return

        publish_time = re.findall(r"time: '(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'?", resp.text)
        publish_time = publish_time[0] if publish_time else ''
        author = trim(''.join(re.findall(r"name: '(\w+)'?", resp.text)))
        tag = ','.join(re.findall(r'{"name":"(\w+)"}\]?', resp.text))

        content = ''.join(re.findall(r"content: '(.+)'?", resp.text))
        if content:
            content = trim(content)
            content = re.sub('[&lt&gt&quot;pa-z\/#3D\.-:_]', '', content)
            content = '。&&&'.join(content.split('。'))
        else:
            return
        content = filter_(content)
        logger.debug('\033[96m title:{}; href:{}; content:{} \033[0m'
                             .format(title, href, len(content)))

        return {
            'category': 'news',
            'site': self.url,
            'tag': tag,
            'news_url': href,
            'title': title,
            'content': content,
            'author': author,
            'publish_time': publish_time,
        }


if __name__ == '__main__':
    TouTiao().parse()

