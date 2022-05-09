from scrapy import Spider
from scrapy.http import Request

class DynamicWebsiteSpider(Spider):
    # Metadata
    name = 'dynamic_website'
    allowed_domains = ['nuvasive.avature.net']
    start_urls = ['https://nuvasive.avature.net/careers/SearchJobs/?jobOffset=0']

    # Custom data

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse(self, response, **kwargs):
        jobs = response.xpath('//li[@class="jobResultItem"]')
        for job in jobs:
            url = job.xpath('.//h3/a/@href').extract_first()
            yield Request(url=url, callback=self.parse_job)

        # process next age
        next_page_url = response.xpath('//a[@class="paginationItem paginationNextLink"]/@href').extract_first()
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(url=absolute_next_page_url)

    def parse_job(self, response, **kwargs):
        url = response.url
        title = response.xpath('//h2[@class="pageTitle1 color1 detailJob"]/text()').extract_first()
        description = response.xpath('//div[@class="jobDetailDescription"]').extract_first()
        apply_link = response.xpath('//div[@class="tPad1 jobButtonSet"]/a/@href').extract_first()

        yield {
            'rid': url.split("/")[-1],
            'url': url,
            'title': title,
            'description': description,
            'apply_link': apply_link,
        }

