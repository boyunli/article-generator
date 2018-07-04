import re
from lxml import etree

from python.requests_pkg import request_get as rget
from python.utils import trim
from python.settings_dev import logger
from python.pipelines import NewsPipeline

class Wechat():
    '''
    爬取搜狗微信热门新闻
    '''
    def __init__(self):
        self.url = 'http://weixin.sogou.com/'

    def parse(self):
        #时尚, 八卦, 旅游, 养生
        categorys = [9, 4, 11, 2]
        purl = 'http://weixin.sogou.com/pcindex/pc/pc_{category}/{page}.html'
        for category in categorys:
            urls = [purl.format(page=page, category=category) for page in range(1, 5)]
            urls.insert(0, 'http://weixin.sogou.com/pcindex/pc/pc_{category}/pc_{category}.html'.format(category=category))
            for url in urls:
                resp = rget(url)
                if not resp: continue
                html = etree.HTML(resp.content)
                hrefs = html.xpath('//ul[@id="pc_0_0"]//li/div[@class="txt-box"]/h3/a/@href')
                if not hrefs:
                    hrefs = html.xpath('//li/div[@class="img-box"]/a/@href')
                if not hrefs:
                    import pdb;pdb.set_trace()
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
        if not resp: self._extract(href, referer=referer)
        html = etree.HTML(resp.content)
        if not html: return

        title = ''.join(html.xpath('//*[@id="activity-name"]/text()'))
        if title:
            title = trim(title)
        else:
            return

        publish_time = re.findall(r'publish_time = "(\d{4}-\d{2}-\d{2})"?', resp.text)
        publish_time = publish_time[0] if publish_time else ''
        author = trim(''.join(html.xpath('//*[@id="js_name"]/text()')))

        content = ''.join(html.xpath('//*[@id="js_content"]//text()'))
        if content:
            content = trim('。&&&'.join(content.split('。')))
        else:
            return
        logger.debug('\033[96m title:{}; href:{}; content:{} \033[0m'
                             .format(title, href, len(content)))

        return {
            'category': 'news',
            'site': self.url,
            'tag': -1,
            'news_url': href,
            'title': title,
            'content': content,
            'author': author,
            'publish_time': publish_time,
        }


if __name__ == '__main__':
    Wechat().parse()

