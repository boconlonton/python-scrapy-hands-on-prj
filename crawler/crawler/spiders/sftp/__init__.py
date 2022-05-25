from abc import ABC

from scrapy.settings import overridden_settings

from crawler.spiders import BaseSpider
from crawler.spiders import MissingAttributeError


class BaseSftpSpider(BaseSpider, ABC):

    file_name = ''

    # Additional
    host_name = None
    username = None
    password = None
    directory = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_attribute()

    def validate_attribute(self):
        check_list = ['host_name', 'username', 'password', 'directory']
        for attr in check_list:
            if getattr(self, attr) is None:
                raise MissingAttributeError(f'Missing Attribute: {attr}')

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings)
        cls.custom_settings['ITEM_PIPELINES']['crawler.pipelines'
                                              '.SftpPipeline'] = 100
        settings.setdict(cls.custom_settings, priority='spider')
