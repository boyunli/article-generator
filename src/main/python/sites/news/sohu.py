import time

from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class SoHu():
    '''
    每一个小时爬一次
    爬取头条热点新闻
    '''
    def __init__(self):
        self.url = 'http://m.sohu.com'

    def parse(self):
        url = 'http://m.sohu.com/ch/23/'
        resp = rget(url)
        html = etree.HTML(resp.content)
        hrefs = html.xpath('//div[@class="swiper-wrapper"]/div/a/@href') + \
            html.xpath('//ul[@class="feed-list-area"]//li/a/@href')
        if not hrefs:
            self.parse()
        details = []
        for href in hrefs:
            if href.startswith('http'): continue
            time.sleep(1)
            try:
                href = urljoin(self.url, href)
                logger.debug("\033[92m 开始爬取:{} \033[0m".format(href))
                item = self._extract(href, url)
                if not item: continue
                details.append(item)
            except IndexError:
                # 像这种很可能是网络原因 导致失败，需要将失败的href写入 某个队列中，待重爬
                continue
        NewsPipeline().save(details)

    def _extract(self, href, referer):
        resp = rget(href, referer=referer)
        if not resp: self._extract(href, referer=referer)
        html = etree.HTML(resp.content)
        if not html: return

        title = ''.join(html.xpath('//h2[@class="title-info"]/text()'))
        if title:
            title = trim(title)
        else:
            return

        publish_time = trim(''.join(html.xpath('//footer[@class="time"]/text()')))
        author = trim(''.join(html.xpath('//header[@class="name"]/text()')))

        content = html.xpath('//div[@class="display-content"]//p/text()') + \
            html.xpath('//div[@class="hidden-content hide"]//p/text()')
        content = ''.join(content)
        if content:
            content = trim('。&&&'.join(content.split('。')))
        else:
            return
        content = filter_(content)
        logger.debug('\033[96m title:{}; href:{}; content:{} \033[0m'
                             .format(title, href, len(content)))

        return {
            'category': 'news',
            'site': self.url,
            'tag': '-1',
            'news_url': href,
            'title': title,
            'content': content,
            'author': author,
            'publish_time': publish_time,
        }


if __name__ == '__main__':
    SoHu().parse()

