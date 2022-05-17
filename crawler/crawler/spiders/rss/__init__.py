import base64

from lxml.etree import XMLParser
from lxml.etree import fromstring

from scrapy import Spider
from scrapy import Request

from scrapy.selector import Selector

from scrapy.exceptions import CloseSpider

from crawler.items import Job


class RssSpider(Spider):
    # Metadata
    IS_PUBLIC = True
    HAS_CDATA = False
    HAS_NAMESPACE = False

    # Additional Information
    # Mandatory when IS_PUBLIC=False
    FEED_URL = ''
    USERNAME = ''
    PASSWORD = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_id = kwargs.get('company_id')
        self.scrape_id = kwargs.get('scrape_id')
        self.start_url = kwargs.get('start_url')
        self.ats_name = kwargs.get('ats_name')

        self.parent_node = kwargs.get('parent_node')

        self.rid = kwargs.get('rid')
        self.apply_url = kwargs.get('apply_url')
        self.detail_url = kwargs.get('detail_url')
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.requirements = kwargs.get('requirements')
        self.job_type = kwargs.get('requirements')
        self.location = kwargs.get('location')
        self.street_address = kwargs.get('street_address')
        self.city = kwargs.get('city')
        self.state = kwargs.get('state')
        self.postal_code = kwargs.get('postal_code')
        self.country = kwargs.get('country')
        self.custom_categories = kwargs.get('custom_categories')
        self.department = kwargs.get('department')
        self.brand = kwargs.get('brand')
        self.company_name = kwargs.get('company_name')

    def start_requests(self):
        if self.IS_PUBLIC:
            yield Request(url=self.start_url)
        else:
            key = base64.b64encode(f'{self.USERNAME}:{self.PASSWORD}'
                                   .encode('ASCII')).decode('utf-8')
            basic_auth = f"Basic {key}"
            self.logger.info(f'Basic Auth: {basic_auth}')
            yield Request(url=self.FEED_URL,
                          headers={
                              'Authorization': basic_auth
                          })

    def extract_parent_node(self, response):
        if self.parent_node:
            if self.HAS_CDATA:
                parser = XMLParser(strip_cdata=False)
                root = fromstring(response.body,
                                  parser=parser,
                                  base_url=response.url)
                selector = Selector(root=root)
                return selector.xpath(f'//{self.parent_node}')
            elif self.HAS_NAMESPACE:
                root = fromstring(response.text.encode('utf8'))
                for ns, val in root.nsmap.items():
                    response.selector.register_namespace(ns, val)
            return response.xpath(f'//{self.parent_node}')
        else:
            raise CloseSpider('Missing parent node')

    def extract_rid(self, item):
        return item.xpath(f'.//{self.rid}/text()').get()

    def extract_apply_url(self, item):
        return item.xpath(f'.//{self.apply_url}/text()').get()

    def extract_detail_url(self, item):
        return item.xpath(f'.//{self.detail_url}/text()').get()

    def extract_title(self, item):
        return item.xpath(f'.//{self.title}/text()').get()

    def extract_description(self, item):
        return item.xpath(f'.//{self.description}/text()').get()

    def extract_requirements(self, item):
        return item.xpath(f'.//{self.requirements}/text()').get()

    def extract_job_type(self, item):
        return item.xpath(f'.//{self.job_type}/text()').get()

    def extract_custom_categories(self, item):
        return item.xpath(f'.//{self.custom_categories}/text()').get()

    def extract_department(self, item):
        return item.xpath(f'.//{self.department}/text()').get()

    def extract_brand(self, item):
        return item.xpath(f'.//{self.brand}/text()').get()

    def extract_company_name(self, item):
        return item.xpath(f'.//{self.company_name}/text()').get()

    def extract_location(self, item):
        if self.location:
            return item.xpath(f'.//{self.company_name}/text()').get()
        else:
            components = [
                self.street_address,
                self.city,
                self.state,
                " ".join(s for s in [self.state, self.postal_code] if s),
                self.country]
            return ", ".join(c for c in components if c)

    def extract_street_address(self, item):
        return item.xpath(f'.//{self.street_address}/text()').get()

    def extract_city(self, item):
        return item.xpath(f'.//{self.city}/text()').get()

    def extract_state(self, item):
        return item.xpath(f'.//{self.state}/text()').get()

    def extract_postal_code(self, item):
        return item.xpath(f'.//{self.postal_code}/text()').get()

    def extract_country(self, item):
        return item.xpath(f'.//{self.country}/text()').get()

    def parse(self, response, *ars, **kwargs):
        jobs = self.extract_parent_node(response)
        for job in jobs:
            yield Job(
                rid=self.extract_rid(job),
                apply_url=self.extract_apply_url(job),
                detail_url=self.extract_detail_url(job),
                title=self.extract_title(job),
                description=self.extract_description(job),
                requirements=self.extract_requirements(job),
                job_type=self.extract_job_type(job),
                custom_categories=self.extract_custom_categories(job),
                department=self.extract_department(job),
                brand=self.extract_brand(job),
                company_name=self.extract_company_name(job)
            )
