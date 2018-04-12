from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class Wbzj():

    def __init__(self):
        self.site = '腕表之家'
        self.site_url = 'http://news.xbiao.com/auction/'

    def parse(self):
        resp = rget(self.site_url)
        html = etree.HTML(resp.content)
        typeHrefs = html.xpath('//div[@class="sub_nav"]/div[@class="wrapper"]/ul/li//a/@href')

        for url in typeHrefs:
            pages = [urljoin(url, 'p{}.html'.format(page)) for page in range(1, 5)]
            pages[0] = url
            details = []
            for page_url in pages:
                resp = rget(page_url)
                if not resp: continue
                html = etree.HTML(resp.content)

                hrefs = set(html.xpath('//dl[position()<last()]//a/@href|//a/@href'))
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

        title = html.xpath('//*[@class="title"]/h1/text()')
        if title:
            title = title[0]
        else:
            return

        tag = html.xpath('//*[@class="breadcrumb left"]/p/a[2]/text()')
        tag = tag[0] if tag else '-1'
        publish_time = html.xpath('//*[@class="article-attr"]/span[1]/text()')
        publish_time = publish_time[0] if publish_time else ''
        author = html.xpath('//*[@class="article-attr"]/span[4]/text()')
        author = author[0].split('：')[1] if author else ''

        ps = html.xpath('//*[@class="article"]//p')
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
                 if ''.join(p.xpath('.//text()'))]
        second = trim('&&&'.join(sText))
        third = trim(''.join(last))

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
            'author': author,
            'publish_time': publish_time,
        }




if __name__ == '__main__':
    Wbzj().parse()

