from crawler.spiders import BaseSpider
from crawler.spiders import MissingAttributeError


class BaseSftpSpider(BaseSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.SftpPipeline': 100
        }
    }

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
