import scrapy
import base64

from crawler.items import Job


class TowneparkSpider(scrapy.Spider):
    # Metadata
    name = 'townepark'

    # Custom data
    FEED_URL = ('https://wd5-impl-services1.workday.com/ccx/service/'
                'customreport2/townepark1/ISU_PDX_Jobs'
                '/INT_PDX_Jobs?format=simplexml')
    USERNAME = 'ISU_PDX_Jobs'
    PASSWORD = 'April2022!!Paradox'

    def start_requests(self):
        key = {base64.b64encode(f'{self.USERNAME}:{self.PASSWORD}'
                                .encode('ASCII')).decode('utf-8')}
        basic_auth = f"Basic {key}"
        self.logger.info(f'Basic Auth: {basic_auth}')
        yield scrapy.Request(url=self.FEED_URL,
                             headers={
                                 'Authorization': basic_auth
                             })

    def parse(self, response, **kwargs):
        response.selector.remove_namespaces()
        jobs = response.xpath('//Report_Entry')
        for job in jobs:
            yield Job(
                rid=job.xpath('.//jobid/text()').get(),
                title=job.xpath('.//title/text()').get(),
                url=job.xpath('.//apply-url/text()').get(),
            )
