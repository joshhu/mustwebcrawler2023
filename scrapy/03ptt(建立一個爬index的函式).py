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
        for b in self.all_boards[:1000]:
            yield scrapy.Request(url=f"https://www.ptt.cc/bbs/{b}/index.html", cookies={'over18': '1'}, callback=self.parse_index)
            
    def parse_index(self, response):
        max_url =response.xpath('//*[@id="action-bar-container"]/div/div[2]//a[2]/@href').extract_first()
        if max_url:
            pass
        else:
            print(response.url)