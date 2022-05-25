from scrapy.http import Request

from crawler.items import Job

from crawler.spiders.sftp import BaseSftpSpider


class SftpSpider(BaseSftpSpider):
    # Metadata
    name = 'sftp'

    # Additional
    host_name = 'ft42.paradox.ai'
    username = 'valvolineuser'
    password = 'KV3scl_qwepa!slQcla8'
    directory = 'valvolineuser/prod'

    def start_requests(self):
        yield Request(url=f'file://{self.file_name}')

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
