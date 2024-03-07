import re

import scrapy
from urllib.parse import urlencode, urljoin

from itemloaders import ItemLoader
from scrapy.exceptions import CloseSpider

from phones_parser.items import PhonesParserItem


class OzonPhonesSpider(scrapy.Spider):
    name = "ozon_phones"
    allowed_domains = ["www.ozon.ru"]
    start_urls = ["https://www.ozon.ru/category/smartfony-15502/?page=1&sorting=rating"]

    def __init__(self, *args, **kwargs):
        super(OzonPhonesSpider, self).__init__(*args, **kwargs)
        self.counter = 0
        self.page = 1

    def paginate_page(self):
        return "https://www.ozon.ru/category/smartfony-15502/?%s" % urlencode({"page": self.page, "sorting": "rating"})

    def parse(self, response):
        links = response.css("div.widget-search-result-container.i7x > .xi7 > .vi6.v6i > .iv7 > a::attr(href)").getall()
        print("parsed_url=", response.url, "phone_cards=", links)
        for link in links:
            self.counter += 1
            if self.counter > 100:
                break
            print("!!!!", self.counter, link)
            yield response.follow(link, callback=self.parse_phone)
        else:
            self.page += 1
            print("!!next!!=", self.paginate_page())
            yield response.follow(self.paginate_page(), callback=self.parse)

    def parse_phone(self, response):
        print("start parse_phone ", response.url)
        loader = ItemLoader(item=PhonesParserItem(), selector=response)
        os_xpath = response.xpath("//dt[span[contains(text(), 'Операционная система')]]/following-sibling::dd//text()").get().strip()
        print("os_xpath=", os_xpath)
        print("raw_version=", response.xpath("//dt[span[contains(text(), 'ерсия')]]/following-sibling::dd//text()").get())
        version_xpath = re.sub(os_xpath, "", response.xpath("//dt[span[contains(text(), 'ерсия')]]/following-sibling::dd//text()").get())
        print("version_xpath=", version_xpath)

        loader.add_value("os", os_xpath)
        loader.add_value("version", version_xpath)
        loader.add_value("url", response.url)
        item = loader.load_item()
        print("item=", item)
        yield item
