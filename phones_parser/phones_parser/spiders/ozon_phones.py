from typing import Iterable
from urllib.parse import urlencode

import scrapy
from itemloaders import ItemLoader
from scrapy import Request

from phones_parser.items import PhonesParserItem


class OzonPhonesSpider(scrapy.Spider):
    TOTAL_ITEMS_COUNT = 10
    name = "ozon_phones"
    allowed_domains = ["www.ozon.ru"]
    start_url = "https://www.ozon.ru/category/smartfony-15502/"

    def __init__(self, *args, **kwargs):
        super(OzonPhonesSpider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.page = 1
        self.start_urls = [self.get_paginated_page()]

    def get_paginated_page(self):
        return f'{self.start_url}?{urlencode({"page": self.page, "sorting": "rating"})}'

    def parse(self, response):
        links = response.css("div.widget-search-result-container.i7x > .xi7 > .vi6.v6i > .iv7 > a::attr(href)").getall()
        print(f"{links=} ", len(links))
        for link in links:
            self.counter += 1
            if self.counter > self.TOTAL_ITEMS_COUNT:
                break

            print("link = ", self.counter, link)
            yield response.follow(link, callback=self.parse_phone)
        else:
            self.page += 1
            print("page =", self.get_paginated_page())
            yield response.follow(self.get_paginated_page(), callback=self.parse)

    @staticmethod
    def xpath_lookup_filter(value: str) -> str:
        return f"//dt[span[contains(text(), '{value}')]]/following-sibling::dd//text()"

    def parse_phone(self, response):
        loader = ItemLoader(item=PhonesParserItem(), selector=response)
        os_xpath = self.xpath_lookup_filter('Операционная система')
        version_xpath = self.xpath_lookup_filter('ерсия')

        loader.add_xpath("os", os_xpath)
        loader.add_xpath("version", version_xpath)

        item = loader.load_item()
        print("item = ", item)
        yield item
