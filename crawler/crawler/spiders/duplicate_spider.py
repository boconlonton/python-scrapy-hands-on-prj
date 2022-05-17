from collections import defaultdict

import scrapy

# import json

# from lxml.etree import XMLParser
# from lxml.etree import fromstring


class DuplicateSpiderSpider(scrapy.Spider):
    # Metadata
    name = 'duplicate_spider'
    start_urls = ['https://mpwpublicdocs.blob.core.windows.net/silkroad/JobPosting.xml']

    # Custom data

    def parse(self, response, **kwargs):
        # CDATA
        # parser = XMLParser(strip_cdata=False)
        # root = fromstring(response.body, parser=parser, base_url=response.url)
        # selector = Selector(root=root)
        # jobs = selector.xpath('//Report_Data//Report_Entry')
        # Get namespace
        # namespace_root = fromstring(response.text.encode('utf8'))
        # for ns, val in namespace_root.nsmap.items():
        #     response.selector.register_namespace(ns, val)
        jobs = response.xpath('//z:row')
        dup_dict = defaultdict(int)
        id_set = set()
        cnt = 0
        for job in jobs:
            cnt += 1
            job_id = job.xpath('./@c2/text()').get()
            if job_id in id_set:
                dup_dict[job_id] += 1
            else:
                id_set.add(job_id)
        self.logger.info(cnt)
        yield dup_dict
