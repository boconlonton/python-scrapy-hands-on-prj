from crawler.spiders.rss import RssSpider


class TowneparkSpider(RssSpider):
    # Metadata
    name = 'townepark'
    IS_PUBLIC = False
    HAS_NAMESPACE = True

    # Custom data
    FEED_URL = ('https://wd5-impl-services1.workday.com/ccx/service/customr'
                'eport2/townepark1/ISU_PDX_Jobs/INT_PDX_Jobs?format=simplexml')
    USERNAME = 'ISU_PDX_Jobs'
    PASSWORD = 'April2022!!Paradox'
