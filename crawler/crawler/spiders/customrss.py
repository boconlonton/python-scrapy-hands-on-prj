from scrapy import Spider

from scrapy import Request


class CustomRssSpider(Spider):
    name = 'customrss'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_url = kwargs.get('start_url')
        self.parent_node = kwargs.get('parent_node')
        self.rid = kwargs.get('rid')
        self.title = kwargs.get('title')

    def start_requests(self):
        yield Request(url=self.start_url)

    def extract_parent_node(self, response):
        return response.xpath(f'//{self.parent_node}')

    def extract_rid(self, item):
        return item.xpath(f'.//{self.rid}/text()').get()

    def extract_title(self, item):
        return item.xpath(f'.//{self.title}/text()').get()

    def parse(self, response, *ars, **kwargs):
        jobs = self.extract_parent_node(response)
        for job in jobs:
            yield {
                'rid': self.extract_rid(job),
                'title': self.extract_title(job),
            }
