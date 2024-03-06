import scrapy


class OzonPhonesSpider(scrapy.Spider):
    name = "ozon_phones"
    allowed_domains = ["www.ozon.ru"]
    start_urls = ["https://www.ozon.ru/category/telefony-i-smart-chasy-15501/?sorting=rating"]

    def parse(self, response):
        print(response)
