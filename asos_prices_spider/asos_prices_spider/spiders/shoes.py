import scrapy


class ShoesSpider(scrapy.Spider):
    name = 'shoes'
    allowed_domains = ['asos.com']
    start_urls = ['https://www.asos.com/men/shoes-boots-trainers/cat/?cid=4209&nlid=mw|shoes|shop+by+product|view+all']

    def parse(self, response):
        shoes_urls = response.xpath('//article[@data-auto-id="productTile"]/a/@href').extract()
        for url in shoes_urls:
            yield Request

