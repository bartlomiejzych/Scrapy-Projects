import json
from scrapy import Spider
from scrapy.http import Request


class ShoesSpider(Spider):
    name = 'shoes'
    allowed_domains = ['asos.com']
    start_urls = ['https://www.asos.com/men/shoes-boots-trainers/cat/?cid=4209&nlid=mw|shoes|shop+by+product|view+all']

    def parse(self, response):
        product_urls = response.xpath('//article[@data-auto-id="productTile"]/a/@href').extract()
        for url in product_urls:
            yield Request(
                        url,
                        callback=self.parse_product,
                        )
        next_page_url = response.xpath('//a[text()="Load more"]/@href').extract_first()
        if next_page_url:
            yield Request(
                        next_page_url,
                        callback=self.parse,
                        )

    def parse_product(self, response):

        product_name = response.xpath('//h1/text()').extract_first()
        product_id = response.url.split('/prd/')[1].split('?')[0]
        price_api_url = 'https://www.asos.com/api/product/catalogue/v3/stockprice?productIds=' + product_id + '&store=COM&currency=GBP'

        yield Request(
                    price_api_url,
                    meta={'product_name': product_name},
                    callback=self.parse_product_price,
                    )

    def parse_product_price(self, response):
        jsonresponse = json.loads(response.body.decode('utf-8'))

        price = jsonresponse[0]['productPrice']['current']['text']

        yield{
            'product_name': response.meta['product_name'],
            'price': price,
            }
