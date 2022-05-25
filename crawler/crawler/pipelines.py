import os
import json

from io import BytesIO

from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem

from paramiko import SFTPClient
from paramiko import Transport

from tempfile import NamedTemporaryFile

from crawler.utils.aws import S3Client

from crawler.spiders import BaseSpider

from crawler.spiders.sftp import BaseSftpSpider


class ItemValidationPipeline:

    def __init__(self):
        self.rids_seen = set()
        self.duplicates = 0

    def process_item(self, item: ItemAdapter, *args, **kwargs):
        adapter = ItemAdapter(item)
        if adapter['rid'] in self.rids_seen:
            self.duplicates += 1
            raise DropItem
        else:
            self.rids_seen.add(adapter['rid'])
            return item

    def close_spider(self, spider: BaseSpider, *args, **kwargs):
        if self.duplicates > 0:
            spider.logger.info(f"DUPLICATED: {self.duplicates} jobs")


class SftpPipeline:

    def __init__(self):
        self.fo = NamedTemporaryFile()

    def open_spider(self, spider: BaseSftpSpider, *args, **kwargs):
        spider.logger.info("SFTP PIPELINE")
        with Transport((spider.host_name, 22)) as transport:
            transport.connect(None,
                              username=spider.username,
                              password=spider.password)

            with SFTPClient.from_transport(transport) as sftp_client:
                spider.logger.info('Connection successfully established...')
                list_files = sftp_client.listdir_attr(spider.directory)
                list_files.sort(key=lambda f: f.st_mtime, reverse=True)
                newest_feed = list_files[0]
                sftp_client.getfo(f'{spider.directory/{newest_feed.filename}}',
                                  self.fo)
                spider.file_name = self.fo.name

    def close_spider(self, *args, **kwargs):
        self.fo.close()


class S3UploadPipeline:

    def __init__(self):
        self._item_pool = list()
        self._stream = BytesIO()
        self.s3_client = S3Client(access_key=os.getenv('AWS_ACCESS_KEY'),
                                  secret_key=os.getenv('AWS_SECRET_KEY'),
                                  bucket_name=os.getenv('AWS_S3_BUCKET'),
                                  region_name=os.getenv('AWS_REGION_NAME'))

    def process_item(self, item: ItemAdapter, *args, **kwargs):
        self._item_pool.append(item)
        return item

    def close_spider(self, spider: BaseSpider):
        """Write to S3"""
        json.dump(self._item_pool, self._stream)
        file_name = f'{spider.company_id}_{spider.scrape_id}.json'
        self.s3_client.login()
        self.s3_client.upload(data=self._stream,
                              file_name=file_name)
        spider.logger.info(f"S3 - {file_name}")
