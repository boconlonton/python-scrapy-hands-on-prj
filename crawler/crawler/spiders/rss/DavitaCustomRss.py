from crawler.spiders.rss import BaseRssSpider


class DavitaCustomRssSpider(BaseRssSpider):
    name = "davita_custom_rss"

    IS_PUBLIC = False
    HAS_NAMESPACE = True
    MISSING_NAMESPACE_DEFINITION = True

    FEED_URL = ('https://wd2-impl-services1.workday.com/ccx/service/c'
                'ustomreport2/davita2/dbostic-impl/Paradox_-_Open_R'
                'equisitions_RAAS?format=simplexml')
    USERNAME = 'ISU_Paradox_Integration'
    PASSWORD = 'TestISU2!!'
