
from time import sleep
from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector

class XmlSpider(Spider):
    name = 'xml'
    allowed_domains = ['www.appone.com']
    start_urls = ['https://www.appone.com/branding/adfeed/default.asp?servervar=ValvolineInstantOilChange.AdFeed.appone.com&all=yes&accesscode=any']

    def parse(self, response, **kwargs):
        jobs = response.xpath('//Job')
       

        for job in jobs:
            id = job.xpath('.//JobID/text()').extract_first()
            title = job.xpath('.//Title/text()').extract_first()
            category = job.xpath('.//Category/text()').extract_first()
            description = job.xpath('.//Description/text()').extract_first()

            yield {
                'id' : id,
                'title': title,
                'category': category,
                'description': description,
            }

        self.logger.info(len(jobs))