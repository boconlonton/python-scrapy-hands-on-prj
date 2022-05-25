from crawler.spiders.rss import BaseRssSpider


class TowneparkSpider(BaseRssSpider):
    # Metadata
    name = 'townepark'
    is_public = False
    has_namespace = True

    # Custom data
    username = 'ISU_PDX_Jobs'
    password = 'April2022!!Paradox'
