import scrapy
from itemloaders import ItemLoader

from phones_parser.items import PhonesParserItem
from phones_parser.mixins import BasePaginationMixin
from phones_parser.services import xpath_lookup_filter
from phones_parser.spiders.constants import START_URL


class OzonPhonesPaginationMixin(BasePaginationMixin):
    start_url = START_URL

    def get_query_params(self):
        return {**super().get_query_params(), "sorting": "rating"}


class OzonPhonesSpider(OzonPhonesPaginationMixin, scrapy.Spider):
    TOTAL_ITEMS_COUNT = 10
    name = "ozon_phones"
    allowed_domains = ["www.ozon.ru"]

    def __init__(self, *args, **kwargs):
        super(OzonPhonesSpider, self).__init__(*args, **kwargs)
        self.counter = 0

    def parse(self, response):
        links = response.css("div.widget-search-result-container.i7x > .xi7 > .vi6.v6i > .iv7 > a::attr(href)").getall()

        for link in links:
            self.counter += 1
            if self.counter > self.TOTAL_ITEMS_COUNT:
                break

            yield response.follow(link, callback=self.parse_phone)
        else:
            self.page += 1
            yield response.follow(self.get_paginated_page(), callback=self.parse)

    def parse_phone(self, response):
        loader = ItemLoader(item=PhonesParserItem(), selector=response)
        os_xpath = f"{xpath_lookup_filter('Операционная система')}//text()"
        version_xpath = f"{xpath_lookup_filter('ерсия')}//text()"

        loader.add_xpath("os", os_xpath)
        loader.add_xpath("version", version_xpath)

        item = loader.load_item()
        yield item
