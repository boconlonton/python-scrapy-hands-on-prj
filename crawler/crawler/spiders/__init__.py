import os

from abc import ABC

from scrapy import Spider


class MissingAttributeError(Exception):
    pass


class BaseSpider(Spider, ABC):
    company_id = None
    scrape_id = None
    session_id = None

    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.ItemValidationPipeline': 200
        }
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company_id = kwargs.get('company_id')
        self.scrape_id = kwargs.get('scrape_id')

        self.start_url = kwargs.get('start_url')
        self.ats_name = kwargs.get('ats_name')

    @classmethod
    def update_settings(cls, settings):
        if os.environ.get('ENV') == 'production':
            cls.custom_settings['ITEM_PIPELINES']['crawler.pipelines'
                                                  '.S3UploadPipeline'] = 1000
            settings.setdict(cls.custom_settings, priority='spider')
