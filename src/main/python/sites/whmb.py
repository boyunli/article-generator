from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class Whmb():

    def __init__(self):
        self.site = '万汇名表'
        self.site_url = 'http://www.ekon.cn/rolex/news.html'

    def parse(self):
        pages_url = [self.site_url]
        pages_url += [urljoin(self.site_url, 'newsp{}.html'.format(page)) for page in range(2, 20)]
        for page_url in pages_url:
            details = []
            resp = rget(page_url)
            if not resp: continue
            html = etree.HTML(resp.content)
            hrefs = html.xpath('//div[@id="brand"]/table//tr/td/h3/a/@href')
            for href in hrefs:
                href = urljoin(self.site_url, href)
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

        title = html.xpath('//td[@class="article_title1a"]/h1/text()')
        # title = title if title else html.xpath('//h1[@class="nw"]/text()')
        if title:
            title = title[0]
        else:
            return

        tag = html.xpath('//div[@id="pagecenter"]/table/tr[2]/td[1]/table/tr/td/a[3]/text()')
        tag = tag[0] if tag else '-1'
        publish_time = html.xpath('//td[@align="center"]//text()')
        publish_time = publish_time[0].split('\xa0')[0] if publish_time else '-1'

        ps =  html.xpath('//td[@class="article_title2a"]//p')
        start_index = 0
        start = ps[start_index].xpath('.//text()')
        if not start:
            start_index = 1
            start = ps[start_index].xpath('.//text()')
        last_index = -1
        last = ps[last_index].xpath('.//text()')
        if not last:
            index = -2
            last = ps[index].xpath('.//text()')

        first = trim(''.join(start))
        sText = [''.join(p.xpath('.//text()'))
                 for p in ps[start_index+1:last_index]
                 if trim(''.join(p.xpath('.//text()')))]
        second = trim('&&&'.join(sText))
        if not second: return
        third = trim(''.join(last))

        if filter_(second): return
        logger.debug('\033[96m title:{}; href:{}; tag:{}; first:{}; second:{}; third:{} \033[0m'
                             .format(title, href, tag, len(first), len(second), len(third)))
        return {
            'site': self.site,
            'tag': tag,
            'news_url': href,
            'title': title,
            'first': first,
            'second': second,
            'third': third,
            'author': '',
            'publish_time': publish_time,
        }




if __name__ == '__main__':
    Whmb().parse()

