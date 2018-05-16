from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class Wbsj():

    def __init__(self):
        self.site = '万表世界'
        self.site_url = 'http://china.wbiao.com.cn/news/'

    def parse(self):
        pages_url = [self.site_url]
        pages_url += [urljoin(self.site_url, 'list_{}.html'.format(page)) for page in range(1, 20)]
        for page_url in pages_url:
            details = []
            resp = rget(page_url)
            if not resp: continue
            html = etree.HTML(resp.content)
            hrefs = html.xpath('//div[@class="newlist"]//h6/a[2]/@href')
            for href in hrefs:
                try:
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
        if not html: return

        title = html.xpath('//h1[@class="nw small"]/text()')
        title = title if title else html.xpath('//h1[@class="nw"]/text()')
        if title:
            title = title[0]
        else:
            return

        tag = html.xpath('//div[@class="tags"]/span[3]/a/text()')
        tag = tag[0] if tag else '-1'
        publish_time = html.xpath('//p[@class="nw"]/span[3]/text()')
        publish_time = publish_time[0].split('：')[1] if publish_time else ''
        author = html.xpath('//p[@class="nw"]/span[1]/text()')
        author = author[0].split('：')[1] if author else ''

        divs = html.xpath('//div[@class="ct"]//text()')
        first = third = ''
        sText = [''.join(div) for div in divs if trim(div)]
        second = trim('&&&'.join(sText))
        if not second: return

        if filter_(second): return
        logger.debug('\033[96m title:{}; href:{}; tag:{}; first:{}; second:{}; third:{} \033[0m'
                             .format(title, href, tag, len(first), len(second), len(third)))
        return {
            'category': '手表',
            'site': self.site,
            'tag': tag,
            'news_url': href,
            'title': title,
            'first': first,
            'second': second,
            'third': third,
            'author': author,
            'publish_time': publish_time,
        }




if __name__ == '__main__':
    Wbsj().parse()

