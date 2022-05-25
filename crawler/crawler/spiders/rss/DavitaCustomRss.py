from crawler.spiders.rss import BaseRssSpider


class DavitaCustomRssSpider(BaseRssSpider):
    name = "davita_custom_rss"

    is_public = False
    has_namespace = True
    missing_namespace_definition = True

    username = 'ISU_Paradox_Integration'
    password = 'TestISU2!!'
