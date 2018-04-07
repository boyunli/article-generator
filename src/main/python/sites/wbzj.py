from lxml import etree

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

        details = []
        for url in typeHrefs:
            resp = rget(url)
            if not resp: continue
            html = etree.HTML(resp.content)
            tag = ''
            if 'reviews' in url: tag = '时计鉴赏'

            hrefs = set(html.xpath('//dl[position()<last()]//a/@href|//a/@href'))
            for href in hrefs:
                try:
                    item = self._extract(href, url, tag)
                    if not item: continue
                    details.append(item)
                except IndexError:
                    import pdb;pdb.set_trace()
        NewsPipeline().save(details)

    def _extract(self, href, referer, tag):
        resp = rget(href, referer=referer)
        if not resp: return
        html = etree.HTML(resp.content)
        if not html: return

        title = html.xpath('//*[@class="title"]/h1/text()')
        if title:
            title = title[0]
        else:
            return

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
        sText = [''.join(p.xpath('.//text()')) for p in ps[start_index+1:last_index]]
        second = trim(''.join(sText))
        third = trim(''.join(last))

        logger.debug('\033[96m title:{}; href:{}; first:{}; second:{}; third:{} \033[0m'
                             .format(title, href, len(first), len(second), len(third)))
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

