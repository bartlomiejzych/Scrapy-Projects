from scrapy import Spider
from scrapy.http import Request


class ClasscentralSpider(Spider):
    name = 'classcentral'
    allowed_domains = ['classcentral.com']
    start_urls = ['https://www.classcentral.com/subjects/']

    def __init__(self, subject=None):
        self.subject = subject

    def parse(self, response):
        if self.subject:
            subject_url - response.xpath('//a[contains(@title, "Programming")]/@href').extract_first()
            absolute_subject_url = response.urljoin(subject_url)
            yield Request(
                absolute_subject_url,
                callback=self.parse_subject
                )
        else:
            self.log('Scraping all pages')

    def parse_subject(self, response):
        pass
