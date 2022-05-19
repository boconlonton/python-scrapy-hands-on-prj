from crawler.spiders.rss import RssSpider


class LidCustomRssSpider(RssSpider):
    name = "lid_custom_rss"

    def extract_rid(self, item) -> str:
        original = super().extract_rid(item)
        return original.split('-')[0].strip()
