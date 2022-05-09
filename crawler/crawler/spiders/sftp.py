from scrapy import Spider

from scrapy.http import Request


class SftpSpider(Spider):
    # Metadata
    name = 'sftp'
    allowed_domains = ['*.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.SftpPipeline': 100
        }
    }

    # Additional
    HOST_NAME = 'ft42.paradox.ai'
    USERNAME = 'valvolineuser'
    PASSWORD = 'KV3scl_qwepa!slQcla8'
    DIRECTORY = 'valvolineuser/prod'

    def start_requests(self):
        yield Request(url=f'file://{self.FILENAME}')

    def parse(self, response, **kwargs):
        pass
