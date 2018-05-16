from lxml import etree
from urllib import parse

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class Aruidu():

    def __init__(self):
        self.site = '锐度名品'
        self.site_url = 'http://www.aruidu.com/article_cat.php?id=18'

    def parse(self):
        resp = rget(self.site_url)
        html = etree.HTML(resp.content)
        try:
            total_url = ''.join(html.xpath('//div[@id="pager"]/a[@class="last"]/@href'))
            pages = parse.parse_qs(parse.urlsplit(total_url).query)['page'][0]
        except:
            pages = 12
        urls = self._construct_page_url(int(pages)+1)

        details = []
        for page_url in urls:
            resp = rget(page_url)
            if not resp: continue
            html = etree.HTML(resp.content)

            hrefs = html.xpath('//div[@class="art_cat_box"]/table//a/@href')
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
        if len(html) is None: return

        title = ''.join(html.xpath('//font[@class="f5 f6"]/text()'))
        tag = ''.join(html.xpath('//div[@id="ur_here"]/a[2]/text()'))

        other = ''.join( html.xpath('//font[@class="f3"]/text()')).split('/')
        publish_time = other[1].strip()
        author = other[0].strip() if other[0] else '-1'

        content = ''.join(html.xpath('//div[@class="box_1"]/div//span[string-length(text()) >1]/text()'))
        if not content:
            content = ''.join(html.xpath('//div[@class="box_1"]/div//p[string-length(text()) >1]/text()'))
        content = trim('。&&&'.join(content.split('。')))
        if filter_(content) and not content: return
        logger.debug('\033[96m title:{}; href:{}; tag:{}; content:{}; \033[0m'
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

    def _construct_page_url(self, pages):
        return [self.site_url + '&page={page}'.format(page=page)
                for page in range(1, pages)]


if __name__ == '__main__':
    Aruidu().parse()

