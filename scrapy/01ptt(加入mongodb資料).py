import scrapy

from pymongo import MongoClient
import urllib


class PttSpider(scrapy.Spider):
    pw = urllib.parse.quote_plus("must")  # type: ignore
    mongo_uri = "mongodb://must:" + pw + "@127.0.0.1:12346/"
    client = MongoClient(mongo_uri)
        
    db = client['ptt']
    ptt_boards = db['boards']
    name = "ptt"
    allowed_domains = ["www.ptt.cc"]
    start_urls = ["https://www.ptt.cc"]
    
    all_boards = [item['Board'] for item in ptt_boards.find({}, {'Board': 1})]
    print(len(all_boards))

    def parse(self, response):
        for b in self.all_boards[:20]:
            print(b)
        # pass
