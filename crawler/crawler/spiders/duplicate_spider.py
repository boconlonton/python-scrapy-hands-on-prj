from collections import defaultdict

import scrapy

# import json
#
# from lxml.etree import XMLParser
# from lxml.etree import fromstring
#
# from parsel import Selector


class DuplicateSpiderSpider(scrapy.Spider):
    name = 'duplicate_spider'
    start_urls = ['https://jobs.emersonhospital.org/feeds/download/aggregator']

    def parse(self, response, **kwargs):
        # parser = XMLParser(strip_cdata=False)
        # root = fromstring(response.body, parser=parser, base_url=response.url)
        # selector = Selector(root=root)
        # jobs = selector.xpath('//job')
        jobs = response.xpath('//job')
        dup_dict = defaultdict(int)
        id_set = set()
        cnt = 0
        for job in jobs:
            cnt += 1
            job_id = job.xpath('./detail-url/text()').get()
            if job_id in id_set:
                dup_dict[job_id] += 1
            else:
                id_set.add(job_id)
        self.logger.info(cnt)
        yield dup_dict
