from scrapy import signals
import os


def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_shopping_list']


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()


class UpdateStatsMiddleware(object):
    def __init__(self, crawler):
        self.crawler = crawler
        # register close_spider method as callback for the spider_closed signal
        crawler.signals.connect(self.close_spider, signals.spider_closed)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def get_jobid(self):
        """Gets jobid through scrapyd's SCRAPY_JOB env variable"""
        return os.environ['SCRAPY_JOB']

    def close_spider(self, spider, reason):
        # do your magic here...
        spider.log('Finishing spider with reason: %s' % reason)
        stats = self.crawler.stats.get_stats()
        jobid = self.get_jobid()
        self.write_job_stats(jobid, stats)

    def write_job_stats(self, jobid, stats):
        # do your magic here...
        pass