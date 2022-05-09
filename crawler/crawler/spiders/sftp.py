from scrapy import Spider

from scrapy.http import Request

from crawler.items import Job


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
        jobs = response.xpath('//job')

        for job in jobs:
            rid = job.xpath('.//jobID/text()').get()
            title = job.xpath('.//title/text()').get()
            category = job.xpath('.//category/text()').get()
            description = job.xpath('.//description/text()').get()

            yield Job({
                'rid': rid,
                'title': title,
                'category_list': [category],
                'description': description,
            })
