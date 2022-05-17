from scrapy import Spider

from crawler.items import Job


class XmlSpider(Spider):
    name = 'xml'
    start_urls = ['https://www.appone.com/branding/adfeed/default.asp?'
                  'servervar=ValvolineInstantOilChange.AdFeed'
                  '.appone.com&all=yes&accesscode=any']

    def parse(self, response, **kwargs):
        jobs = response.xpath('//Job')

        for job in jobs:

            rid = job.xpath('.//JobID/text()').get()
            title = job.xpath('.//Title/text()').get()
            category = job.xpath('.//Category/text()').get()
            description = job.xpath('.//Description/text()').get()

            yield Job({
                'rid': rid,
                'title': title,
                'category_list': [category],
                'description': description,
            })
