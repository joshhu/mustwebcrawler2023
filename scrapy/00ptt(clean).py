import scrapy


class PttSpider(scrapy.Spider):
    name = "ptt"
    allowed_domains = ["www.ptt.cc"]
    start_urls = ["https://www.ptt.cc"]

    def parse(self, response):
        print("明新科技大學資管系")
        # pass