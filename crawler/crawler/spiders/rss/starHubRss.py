
import scrapy
from crawler.items import Job, User, UserType


class starHubRssSpider(scrapy.Spider):
    # meta data
    name = "starhub_rss"
    start_urls = ['https://starhubltdt1.valhalla10'
                  '.stage.jobs2web.com/feed/349960']
    print("This is spider start?")

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)
        print("start_request for each url")

    def parse(self, response, **kwargs):
        jobs = response.xpath('//job')
        x = 0
        for job in jobs:
            x += 1
            rid = job.xpath('.//ID/text()').get()
            title = job.xpath('.//title/text()').get()
            description = job.xpath('.//description/text()').get()
            company = job.xpath('.//company/text()').get()
            city = job.xpath('.//city/text()').get()
            state = job.xpath('.//state/text()').get()
            postalcode = job.xpath('.//postalcode/text()').get()

            job = Job({
                'rid': rid,
                'title': title,
                'description': description,
                'brand': company,
                'city': city,
                'state': state,
                'postal_code': postalcode,
            })

            recruiterEmail = "recruiterTest@gmail.com"
            if recruiterEmail:
                job['users'] = [User(user_type=UserType.Recruiter,
                                     email=recruiterEmail).to_dict()]
            print(recruiterEmail)
            print(f"Parsing Function is here? {x}")
            print(job['users'])
            yield job
