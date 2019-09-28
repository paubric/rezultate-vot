import scrapy
from scrapy import Item, Field
from scrapy.loader import ItemLoader
import json

class ElectionData(Item):
    year = Field()
    type = Field()
    partial = Field()


class AEPSpider(scrapy.Spider):
    name = 'AEPSpider'
    start_urls = ['http://alegeri.roaep.ro/wp-content/plugins/aep/aep_posts.php?qType=post']

    def parse(self, response):
        data = json.loads(response.body)

        for election in data:
            loader = ItemLoader(item=ElectionData())
            loader.add_value('year', election['alegeriDate'])
            loader.add_value('type', election['category'])
            loader.add_value('partial', election['isPartial'])
            yield loader.load_item()
