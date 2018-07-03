import re
from lxml import etree

from python.requests_pkg import request_get as rget
from python.utils import trim, filter_
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class Wechat():
    '''
    爬取搜狗微信热门新闻
    '''
    def __init__(self):
        self.url = 'http://weixin.sogou.com/'

    def parse(self):
        url = 'http://weixin.sogou.com/pcindex/pc/pc_0/{page}.html'
        urls = [url.format(page=page) for page in range(1, 6)]
        urls.insert(0, self.url)

        for url in urls:
            # 获取当天最新120条新闻
            resp = rget(url, referer=self.url)
            if not resp: continue
            html = etree.HTML(resp.content)
            hrefs = html.xpath('//ul[@id="pc_0_0"]//li/div[@class="txt-box"]/h3/a/@href')
            if not hrefs: continue
            logger.debug("\033[92m 开始爬取:{} \033[0m".format(url))
            details = []
            for href in hrefs:
                try:
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

        title = html.xpath('//*[@id="activity-name"]/text()')
        if title:
            title = trim(title[0])
        else:
            return

        publish_time = re.findall(r'publish_time = "(\d{4}-\d{2}-\d{2})"?', resp.text)
        publish_time = publish_time[0] if publish_time else ''
        author = trim(''.join(html.xpath('//*[@id="js_name"]/text()')))

        content = ''.join(html.xpath('//*[@id="js_content"]//text()'))
        if content:
            content = trim('。&&&'.join(content.split('。')))
        else:
            content = ''.join(html.xpath('//div[@class="mcontent"]//text()'))
        if filter_(content) or not content: return
        logger.debug('\033[96m title:{}; href:{}; content:{} \033[0m'
                             .format(title, href, len(content)))

        return {
            'category': 'news',
            'site': 'http://weixin.sogou.com/',
            'tag': -1,
            'news_url': href,
            'title': title,
            'content': content,
            'author': author,
            'publish_time': publish_time,
        }


if __name__ == '__main__':
    Wechat().parse()

