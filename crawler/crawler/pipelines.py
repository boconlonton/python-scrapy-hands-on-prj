# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.exceptions import DropItem


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
