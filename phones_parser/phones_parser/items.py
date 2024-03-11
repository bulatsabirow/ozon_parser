# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
from operator import methodcaller
from typing import Optional

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clean_version_data(raw_version: str) -> Optional[int]:
    """
    Allows to extract the information about the operating system version using regular expression:
    [^\d.]+ detects everything except digits and point (example: '123alp;' -> 'alp;');
    (\..*) detects all symbols after point (including this point) (example: '1.2.5' -> '.2.4').
    """
    version = re.sub(r"([^\d.]+)|(\..*)", "", raw_version)
    try:
        return int(version)
    except ValueError:
        return


class PhonesParserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    os = scrapy.Field(input_processor=MapCompose(methodcaller("strip")), output_processor=TakeFirst())
    version = scrapy.Field(input_processor=MapCompose(clean_version_data), output_processor=TakeFirst())
