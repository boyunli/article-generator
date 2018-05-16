from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class NanRenWo():

    def __init__(self):
        self.site = '男人窝'
        self.site_url = 'https://www.nanrenwo.net/watch/'

    def parse(self):
        resp = rget(self.site_url)
        html = etree.HTML(resp.content)
        typeHrefs = html.xpath('//dl[@class="menu clearfix"]/dd//a/@href')
        typeHrefs = [urljoin(self.site_url, type_) for type_ in typeHrefs]

        for url in typeHrefs:
            if 'news' in url:
                pages = self._construct_pages(url, '73')
            elif 'guide' in url:
                pages = self._construct_pages(url, '74')
            elif 'wiki' in url:
                pages = self._construct_pages(url, '75')
            else:
                pages = self._construct_pages(url, '76')
            pages[0] = url
            details = []
            for page_url in pages:
                resp = rget(page_url)
                if not resp: continue
                html = etree.HTML(resp.content)

                dds =  html.xpath('//dl[@class="list-info"]//dd')
                for dd in dds:
                    try:
                        href = dd.xpath('./h3/a/@href')
                        if href:
                            href = urljoin(page_url, href[0])
                        else: continue
                        tag = ' '.join(dd.xpath('.//div[@class="info-l"]/a/text()'))
                        item = self._extract(href, tag, page_url)
                        if not item: continue
                        details.append(item)
                    except IndexError:
                        # 像这种很可能是网络原因 导致失败，需要将失败的href写入 某个队列中，待重爬
                        continue
                NewsPipeline().save(details)

    def _extract(self, href, tag, referer):
        resp = rget(href, referer=referer)
        if not resp: return
        html = etree.HTML(resp.content)
        if not html: return

        title = html.xpath('//div[@class="main-left fl"]/h1/text()')
        title = title if title else html.xpath('//div[@class="tuku-cont"]/h1/text()')
        if title:
            title = title[0]
        else:
            return

        publish_time = html.xpath('//div[@class="source fl"]/span[@class="item01"]/text()')
        publish_time = publish_time if publish_time else html.xpath('//*[@class="time"]/text()')
        publish_time = publish_time[0].split('\u3000')[0] if publish_time else '-1'
        author = html.xpath('//*[@class="name"]//strong/text()')
        author = author[0] if author else '-1'

        ps = html.xpath('//*[@class="article"]//p/text()')
        if not ps:
            ps = html.xpath('//*[@class="list"]//@data-text')
        sText = ''.join(ps)
        if len(sText) <= 100:
            content = trim(sText)
        else:
            sText = sText.split('。')
            content = trim('。&&&'.join(sText))
        if filter_(content) or not content: return

        logger.debug('\033[96m title:{}; href:{}; tag:{}; content:{}\033[0m'
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

    def _construct_pages(self, url, type_):
        return [urljoin(url, 'list_{type_}_{page}.html'.format(type_=type_, page=page))
                for page in range(1, 10)]


if __name__ == '__main__':
    NanRenWo().parse()

