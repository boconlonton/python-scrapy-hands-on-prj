

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders.rss',
                  'crawler.spiders.api_feed',
                  'crawler.spiders.dynamic_site',
                  'crawler.spiders.sftp',
                  'crawler.spiders.others']
NEWSPIDER_MODULE = 'crawler.spiders'

ROBOTSTXT_OBEY = False

# SPLASH_URL = 'http://192.168.59.103:8050'

# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }

# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
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
# ITEM_PIPELINES = {
#     'crawler.pipelines.ItemValidationPipeline': 200,
# }

# Configure extensions
EXTENSIONS = {
    'crawler.extensions.SentryLogging': -1
}
