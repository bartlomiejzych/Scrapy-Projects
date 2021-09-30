import scrapy


class ShoesSpider(scrapy.Spider):
    name = 'shoes'
    allowed_domains = ['asos.com']
    start_urls = ['http://asos.com/']

    def parse(self, response):
        pass
