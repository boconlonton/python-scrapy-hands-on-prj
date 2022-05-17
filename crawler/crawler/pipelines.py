from itemadapter import ItemAdapter

from scrapy.spiders import Spider

from scrapy.exceptions import DropItem

from paramiko import SFTPClient
from paramiko import Transport

from tempfile import NamedTemporaryFile


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
        self.fo = NamedTemporaryFile()
        with Transport((spider.HOST_NAME, 22)) as transport:
            transport.connect(None,
                              username=spider.USERNAME,
                              password=spider.PASSWORD)

            with SFTPClient.from_transport(transport) as sftp_client:
                spider.logger.info('Connection successfully established...')
                list_files = sftp_client.listdir_attr(spider.DIRECTORY)
                list_files.sort(key=lambda f: f.st_mtime, reverse=True)
                newest_feed = list_files[0]
                sftp_client.getfo(f'{spider.DIRECTORY}/{newest_feed.filename}',
                                  self.fo)
                spider.FILENAME = self.fo.name

    def close_spider(self, spider: Spider):
        spider.logger.info("Delete temporary file...")
        spider.logger.info("Closed")
        self.fo.close()
