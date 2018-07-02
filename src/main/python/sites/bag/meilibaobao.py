from lxml import etree
from urllib.parse import urljoin

from python.requests_pkg import request_get as rget
from python.utils import trim
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class MeiliBaoBao():

    def __init__(self):
        self.site = '美丽包包'
        self.site_url = 'http://meilibaobao.com'

    def parse(self):
        resp = rget('http://meilibaobao.com/artlist-217.html')
        html = etree.HTML(resp.content)

        try:
            last_page = ''.join(html.xpath('//td[@class="pagernum"]/a[last()]/text()'))
            last_page = int(last_page)
        except:
            last_page = 180

        pages = self._construct_pages(last_page+1)
        details = []
        for page_url in pages:
            resp = rget(page_url)
            if not resp: continue
            html = etree.HTML(resp.content)

            divs = html.xpath('//div[@id="columns"]/div')
            for dd in divs:
                try:
                    href = ''.join(dd.xpath('./div[@class="pic"]/a/@href'))
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

        info = html.xpath('//div[@class="info"]/text()')
        tag = info[-1]
        publish_time = info[0].split('\xa0')[0]
        author = ''.join(html.xpath('//div[@class="info"]/a/text()'))

        title = ''.join(html.xpath('//div[@class="article_con"]/h1/text()'))

        content = ''.join(html.xpath('//div[@class="art_con"]//text()'))
        if content:
            content = trim('。&&&'.join(content.split('。')))
        else:
            content = ''.join(html.xpath('//div[@class="mcontent"]//text()'))
        if not content: return
        logger.debug('\033[96m title:{}; href:{}; tag:{}; content:{} \033[0m'
                             .format(title, href, tag, len(content)))
        return {
            'category': '包包',
            'site': self.site,
            'tag': tag,
            'news_url': href,
            'title': title,
            'content': content,
            'author': author,
            'publish_time': publish_time,
        }

    def _construct_pages(self, last):
        return [urljoin(self.site_url, 'artlist-217-{page}.html'.format(page=page))
                for page in range(1, last)]


if __name__ == '__main__':
    MeiliBaoBao().parse()

