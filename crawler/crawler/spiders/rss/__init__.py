import base64

from lxml.etree import XMLParser
from lxml.etree import fromstring
from lxml.etree import QName
from lxml.etree import cleanup_namespaces
from lxml.etree import tostring

from scrapy import Request

from scrapy.selector import Selector

from scrapy.exceptions import CloseSpider

from crawler.items import Job

from crawler.spiders import BaseSpider
from crawler.spiders import MissingAttributeError


class BaseRssSpider(BaseSpider):
    # Metadata
    is_public = True
    has_cdata = False
    has_namespace = False
    missing_namespace_definition = False

    # Additional Information
    # Mandatory when is_public=False
    username = None
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_attribute()

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
        if self.is_public:
            yield Request(url=self.start_url)
        else:
            key = base64.b64encode(f'{self.username}:{self.password}'
                                   .encode('ASCII')).decode('utf-8')
            basic_auth = f"Basic {key}"
            self.logger.info(f'Basic Auth: {basic_auth}')
            yield Request(url=self.start_url,
                          headers={
                              'Authorization': basic_auth
                          })

    def extract_parent_node(self, response):
        if self.parent_node:
            if self.has_cdata:
                parser = XMLParser(strip_cdata=False)
                root = fromstring(response.body,
                                  parser=parser,
                                  base_url=response.url)
                selector = Selector(root=root)
                return selector.xpath(f'//{self.parent_node}')
            elif self.has_namespace:
                root = fromstring(response.text.encode('utf8'))
                if self.missing_namespace_definition:
                    for elem in root.getiterator():
                        elem.tag = QName(elem).localname
                    cleanup_namespaces(root)
                    res = fromstring(tostring(root))
                    selector = Selector(root=res)
                    return selector.xpath(f'//{self.parent_node}')
                else:
                    for ns, val in root.nsmap.items():
                        response.selector.register_namespace(ns, val)
            return response.xpath(f'//{self.parent_node}')
        else:
            raise CloseSpider('Missing parent node')

    def extract_rid(self, item) -> str:
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
        self.logger.info("START PARSING")
        jobs = self.extract_parent_node(response)
        self.logger.info(len(jobs))
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

    def validate_attribute(self):
        if not self.is_public:
            check_list = ['username', 'password']
            for attr in check_list:
                if getattr(self, attr) is None:
                    raise MissingAttributeError(f'Missing Attribute: {attr}')
