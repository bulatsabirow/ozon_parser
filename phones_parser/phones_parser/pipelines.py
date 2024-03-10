# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from itemadapter import ItemAdapter
import pandas as pd

# useful for handling different item types with a single interface


class PhonesParserPipeline:
    def __init__(self, *args, **kwargs):
        super(PhonesParserPipeline, self).__init__(*args, **kwargs)
        self.items = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item.setdefault("os", "Другое")
        item.setdefault('version', None)
        print("adapter = ", adapter.item)
        self.items.append(item)
        return item

    def close_spider(self, spider):
        dataframe = pd.DataFrame(self.items)
        distribution = dataframe.value_counts(sort=True)

        with open(os.path.join("..", "results.csv"), "w", encoding="utf-8") as file:
            file.write(distribution.to_csv())
        print("Results: ", dataframe, distribution, sep="\n")
