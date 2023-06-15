
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from colorama import Fore
from colorama import Style
import urllib



class PttProjectPipeline:
    def open_spider(self, spider):
        self.mongo_uri = "mongodb://must:" + urllib.parse.quote_plus("must") + "@127.0.0.1:12346/"  # type: ignore
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client['ptt']
        self.ptt_items = self.db['ptt_content']


    def process_item(self, item, spider):
        print(f"{Fore.CYAN}{item['post_time']} {Fore.YELLOW}{item['board']}  {Fore.GREEN}{item['title']}{Style.RESET_ALL}")
        return item
