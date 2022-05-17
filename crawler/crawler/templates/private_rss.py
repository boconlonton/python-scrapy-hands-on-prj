import base64

from scrapy import Request

from crawler.templates import PublicRssSpider


class PrivateRssSpider(PublicRssSpider):
    FEED_URL = ''
    USERNAME = ''
    PASSWORD = ''

    def start_requests(self):
        key = {base64.b64encode(f'{self.USERNAME}:{self.PASSWORD}'
                                .encode('ASCII')).decode('utf-8')}
        basic_auth = f"Basic {key}"
        self.logger.info(f'Basic Auth: {basic_auth}')
        yield Request(url=self.FEED_URL,
                      headers={
                          'Authorization': basic_auth
                      })
