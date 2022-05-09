from collections import defaultdict

import scrapy

# import json
#
# from lxml.etree import XMLParser
# from lxml.etree import fromstring
#
# from parsel import Selector


class DuplicateSpiderSpider(scrapy.Spider):
    # Metadata
    name = 'duplicate_spider'
    start_urls = ['file:///home/tan/Downloads/Paradox_Job_Search_Bot_Sample_Feed.xml']
    SCHEDULE_TYPE = 'standard'

    # Custom data

    def parse(self, response, **kwargs):
        # parser = XMLParser(strip_cdata=False)
        # root = fromstring(response.body, parser=parser, base_url=response.url)
        # selector = Selector(root=root)
        # jobs = selector.xpath('//Report_Data//Report_Entry')
        response.selector.register_namespace('wd', 'urn:com.workday.report/Paradox_Job_Search_Bot_Sample_Feed')
        jobs = response.xpath('//wd:Report_Entry')
        dup_dict = defaultdict(int)
        id_set = set()
        cnt = 0
        for job in jobs:
            cnt += 1
            job_id = job.xpath('./wd:Job_Req_ID/text()').get()
            if job_id in id_set:
                dup_dict[job_id] += 1
            else:
                id_set.add(job_id)
        self.logger.info(cnt)
        yield dup_dict
