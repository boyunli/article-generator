import re
from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class MilanStand():

    def __init__(self):
        self.site = '米兰站'
        self.site_url = 'http://www.milanstand.com'

    def parse(self):
        resp = rget('http://www.milanstand.com/article-zixun-1/')
        html = etree.HTML(resp.content)

        try:
            last_page = html.xpath('//p[@class="nx"]/following-sibling::p/a/@href')[0]
            last_page = int(last_page.split('-')[-1][:-1])
        except IndexError:
            last_page = 55

        pages = self._construct_pages(last_page+1)
        details = []
        for page_url in pages:
            resp = rget(page_url)
            if not resp: continue
            html = etree.HTML(resp.content)

            divs = html.xpath('//div[@class="box_3"]/table/tr//div[contains(text(), "手表")]')
            for dd in divs:
                try:
                    href = ''.join(dd.xpath('./a/@href'))
                    href = urljoin(self.site_url, href)
                    item = self._extract(href, page_url)
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
        if len(html) is None: return

        tag = ''.join(html.xpath('//div[@class="h"]/a[last()]/text()'))
        title = ''.join(html.xpath('//font[@class="f5"]/text()'))

        other = trim(''.join(html.xpath('//font[@class="f3"]/text()')))
        other = re.findall('发布时间：(\d{4}-\d{2}-\d{2})来源：(\w+)', other)
        if other:
            publish_time = other[0][0]
            author = other[0][1]
        else:
            publish_time = author = ''

        content = ''.join(html.xpath('//div[@class="mcontent"]//p[string-length(text()) >1]/text()'))
        if content:
            content = trim('。&&&'.join(content.split('。')))
        else:
            content = ''.join(html.xpath('//div[@class="mcontent"]//text()'))
        if filter_(content) or not content: return
        logger.debug('\033[96m title:{}; href:{}; tag:{}; content:{} \033[0m'
                             .format(title, href, tag, len(content)))
        return {
            'category': '手表',
            'site': self.site,
            'tag': tag,
            'news_url': href,
            'title': title,
            'content': content,
            'author': author,
            'publish_time': publish_time,
        }

    def _construct_pages(self, last):
        return [urljoin(self.site_url, 'article-zixun-{page}/'.format(page=page))
                for page in range(1, last)]


if __name__ == '__main__':
    MilanStand().parse()

