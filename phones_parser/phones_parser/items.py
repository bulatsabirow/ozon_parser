# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
from operator import attrgetter, methodcaller

import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags

def clean_data(raw_version: str) -> str:
    return re.sub(r"\..*", "", raw_version).strip()

class PhonesParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    os = scrapy.Field(
        input_processor=MapCompose(methodcaller("strip")),
        output_processor=TakeFirst()
    )
    version = scrapy.Field(
        input_processor=MapCompose(clean_data),
        output_processor=TakeFirst()
    )
    url = scrapy.Field()
