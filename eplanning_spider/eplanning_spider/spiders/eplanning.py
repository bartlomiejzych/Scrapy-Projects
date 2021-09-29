from scrapy import Spider
from scrapy.http import Request

class EplanningSpider(Spider):
    name = 'eplanning'
    allowed_domains = ['eplanning.ie']
    start_urls = ['http://eplanning.ie/']

    def parse(self, response):
        urls = response.xpath('//a/@href').extract()
        for url in urls:
            if '#' == url:
                pass
            else:
                yield Request(
                            url,
                            callback=self.parse_application,
                            )

    def parse_application(self, response):
        app_url = response.xpath(
            '//*[@class="glyphicon glyphicon-inbox btn-lg"]/following-sibling::a/@href').extract_first()
        yield Request(
                    response.urljoin(app_url),
                    callback=self.parse_form,
                    )

    def parse_form(self, request):
        pass