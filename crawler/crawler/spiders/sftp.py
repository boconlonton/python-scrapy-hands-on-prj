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
    HOST_NAME = None
    USERNAME = None
    PASSWORD = None

    def __init__(self,
                 HOST_NAME,
                 USERNAME,
                 PASSWORD,
                 **kwargs):
        super().__init__(**kwargs)
        self.HOST_NAME = HOST_NAME
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.logger.info("Initialization")

    def start_requests(self):
        self.logger.info("Start Crawling")
        yield Request(url=f'file:///home/tan/Downloads/tmp.xml')

    def parse(self, response, **kwargs):
        pass
