from itemadapter import ItemAdapter

from scrapy.spiders import Spider

from scrapy.exceptions import DropItem

from paramiko import SFTPClient
from paramiko import Transport


class DuplicatesPipeline:
    def __init__(self):
        self.rids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['rid'] in self.rids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.rids_seen.add(adapter['rid'])
            return item


class SftpPipeline:

    def open_spider(self, spider: Spider):
        spider.logger.info("Open")
        with Transport((spider.HOST_NAME, 22)) as transport:
            transport.connect(None,
                          username=spider.USERNAME,
                          password=spider.PASSWORD)

            with SFTPClient.from_transport(transport) as sftp_client:
                spider.logger.info('Connection successfully established...')
