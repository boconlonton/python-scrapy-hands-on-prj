import os

from abc import ABC

from scrapy import Spider


class MissingAttributeError(Exception):
    pass


class BaseSpider(Spider, ABC):
    company_id = None
    scrape_id = None
    session_id = None

    if os.environ.get('ENV') == 'production':
        custom_settings = {
            'ITEM_PIPELINES': {
                'crawler.pipelines.S3UploadPipeline': 1000
            }
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
