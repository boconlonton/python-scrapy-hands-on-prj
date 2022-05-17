BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# DOWNLOAD_DELAY = 3

# Enable or disable spider middlewares
# SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerDownloaderMiddleware': 543,
# }

# Configure item pipelines
ITEM_PIPELINES = {
    'crawler.pipelines.DuplicatesPipeline': 300,
}
