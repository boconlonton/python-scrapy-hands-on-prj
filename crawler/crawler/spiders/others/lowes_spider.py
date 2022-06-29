from collections import defaultdict

import scrapy
import html
import re

# import json

from lxml.etree import XMLParser
from lxml.etree import fromstring

from scrapy.selector import Selector


class LowesSpider(scrapy.Spider):
    # Metadata
    name = 'lowes_spider'
    start_urls = ['http://import.brassring.com/WebRouter/WebRouter.asmx/route']

    # Custom data
    def start_requests(self):
        for i in range(1, 250):
            yield scrapy.Request(url=self.start_urls[0],
                                 headers={
                                     'Content-Type': 'application/x-www-form'
                                                     '-urlencoded; charset=utf-8',
                                     'SOAPAction': '"#POST"'
                                 },
                                 method="POST",
                                 body=f"inputXML=%0A%20%20%20%20%20%20%20%20%20%20%20%20%3CEnvelope%20version%3D\'01.00\'%3E%0A%09%20%20%20%20%20%20%20%20%20%20%20%20%3CSender%3E%0A%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CId%3E12345%3C%2FId%3E%0A%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CCredential%3E25239%3C%2FCredential%3E%0A%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FSender%3E%0A%09%20%20%20%20%20%20%20%20%20%20%20%20%3CTransactInfo%20transactId%3D\'1\'%20transactType%3D\'data\'%3E%0A%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CTransactId%3E01%2F27%2F2010%3C%2FTransactId%3E%0A%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CTimeStamp%3E12%3A00%3A00%20AM%3C%2FTimeStamp%3E%0A%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FTransactInfo%3E%0A%09%20%20%20%20%20%20%20%20%20%20%20%20%3CUnit%20UnitProcessor%3D\'SearchAPI\'%3E%0A%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CPacket%3E%0A%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CPacketInfo%20packetType%3D\'data\'%3E%0A%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CpacketId%3E1%3C%2FpacketId%3E%0A%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FPacketInfo%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3CPayload%3E%0A%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CInputString%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CClientId%3E25239%3C%2FClientId%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CSiteId%3E5014%3C%2FSiteId%3E%3CPageNumber%3E{i}%3C%2FPageNumber%3E%3COutputXMLFormat%3E0%3C%2FOutputXMLFormat%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CAuthenticationToken%2F%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CHotJobs%2F%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3CJobDescription%3EYES%3C%2FJobDescription%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CReturnJobDetailQues%3E6862%2C6843%2C6838%2C11848%2C325%2C84%2C254%2C89%2C6863%2C275%2C6839%2C6845%2C12284%2C11847%2C1126%2C93%2C11849%2C280%2C12088%2C12264%2C6844%2C6866%2C9367%2C92%2C7315%2C88%2C11986%2C10698%2C10699%2C10723%2C10724%2C10725%2C10706%2C10703%2C10704%2C12266%2C10726%2C10705%2C11846%2C12440%3C%2FReturnJobDetailQues%3E%3CProximitySearch%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CDistance%2F%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CMeasurement%2F%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CCountry%2F%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CState%2F%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CCity%2F%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CzipCode%2F%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FProximitySearch%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CJobMatchCriteriaText%2F%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CQuestions%3E%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%3CQuestion%20Sortorder%3D\'ASC\'%20Sort%3D\'No\'%3E%0A%09%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3CId%3E12284%3C%2FId%3E%3CValue%3E%0A%09%09%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C!%5BCDATA%5BYES%5D%5D%3E%0A%09%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FValue%3E%0A%09%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FQuestion%3E%0A%09%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FQuestions%3E%0A%09%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FInputString%3E%0A%09%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FPayload%3E%0A%09%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FPacket%3E%0A%09%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FUnit%3E%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C%2FEnvelope%3E")

    def parse(self, response, **kwargs):
        raw_data = re.sub(r'\sxmlns="[^"]+"', '', response.text, count=1)
        parser = XMLParser(strip_cdata=False)
        root = fromstring(raw_data.encode("utf-8"),
                          parser=parser,
                          base_url=response.url)
        selector = Selector(root=root)
        raw_data = selector.xpath('//string').get()
        raw_data = html.unescape(raw_data)
        data = raw_data.replace('<?xml version="1.0" encoding="utf-8"?>', "")
        data = data.replace('<string>', "")
        data = data.replace('</string>', "")
        root2 = fromstring(data.encode("utf-8"),
                           parser=parser)
        selector = Selector(root=root2)
        jobs = selector.xpath('//Job')
        for job in jobs:
            job_id = job.xpath("./Question[@Id='6862']/text()").get()
            street_address = job.xpath("./Question[@Id='11847']/text()").get()
            city = job.xpath("./Question[@Id='11848']/text()").get()
            state = job.xpath("./Question[@Id='11849']/text()").get()
            zip_code = job.xpath("./Question[@Id='280']/text()").get()
            country = job.xpath("./Question[@Id='325']/text()").get()
            yield {
                'rid': job_id,
            }
