from scrapy import Spider

from scrapy.http import Request


class SftpSpider(Spider):
    name = 'sftp'
    allowed_domains = ['*.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.SftpPipeline': 100
        }
    }
    HOST_NAME = 'ft42.paradox.ai'
    USERNAME = 'valvolineuser'
    PASSWORD = 'KV3scl_qwepa!slQcla8'

    def start_requests(self):
        self.logger.info("Start Crawling")
        yield Request(url=f'file:///home/tan/Downloads/tmp.xml')

    def parse(self, response, **kwargs):
        pass
