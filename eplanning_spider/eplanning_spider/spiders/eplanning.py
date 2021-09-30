from scrapy import Spider
from scrapy.http import Request, FormRequest

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

    def parse_form(self, response):
        yield FormRequest.from_response(
                                    response,
                                    formdata={'RdoTimeLimit': '42'},
                                    dont_filter=True,
                                    formxpath='(//form)[2]',
                                    callback=self.parse_pages,
                                    )

    def parse_pages(self, response):
        application_urls = response.xpath('//td/a/@href').extract()
        for url in application_urls:
            url = response.urljoin(url)
            yield Request(
                        url,
                        callback=self.parse_items,
                        )
        next_page_url = response.xpath('//*[@rel="next"]/@href').extract_first()    
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(
                    absolute_next_page_url,
                    callback=self.parse_pages,
                    )

    def parse_items(self, response):
        pass