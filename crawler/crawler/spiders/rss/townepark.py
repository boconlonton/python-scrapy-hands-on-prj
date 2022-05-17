from crawler.templates.private_rss import PrivateRssSpider


class TowneparkSpider(PrivateRssSpider):
    # Metadata
    name = 'townepark'

    # Custom data
    FEED_URL = ('https://wd5-impl-services1.workday.com/ccx/service/'
                'customreport2/townepark1/ISU_PDX_Jobs'
                '/INT_PDX_Jobs?format=simplexml')
    USERNAME = 'ISU_PDX_Jobs'
    PASSWORD = 'April2022!!Paradox'
