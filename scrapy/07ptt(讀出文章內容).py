import scrapy
import os
from pymongo import MongoClient
import urllib
from colorama import Fore
from colorama import Style
from pytz import timezone
from ptt_project.items import PttProjectItem  
from datetime import datetime


class PttSpider(scrapy.Spider):
    pw = urllib.parse.quote_plus("must")  # type: ignore
    mongo_uri = "mongodb://must:" + pw + "@127.0.0.1:12346/"
    client = MongoClient(mongo_uri)
        
    db = client['ptt']
    ptt_boards = db['boards']
    ptt_content = db['ptt_content']
    name = "ptt"
    allowed_domains = ["www.ptt.cc"]
    start_urls = ["https://www.ptt.cc"]
    
    all_boards = [item['Board'] for item in ptt_boards.find({}, {'Board': 1})]
    print(len(all_boards))

    def parse(self, response):
        for b in self.all_boards[:2]:
            yield scrapy.Request(url=f"https://www.ptt.cc/bbs/{b}/index.html", cookies={'over18': '1'}, callback=self.parse_index)
            
    def parse_index(self, response):
        max_url =response.xpath('//*[@id="action-bar-container"]/div/div[2]//a[2]/@href').extract_first()
        if max_url:
            max_page_count = os.path.basename(max_url).split('.')[0].split('index')[1]
            for i in range(1, int(max_page_count)+2):
                url = 'https://www.ptt.cc' + os.path.dirname(max_url) + '/index' + str(i) + '.html'
                yield scrapy.Request(url=url, cookies={'over18': '1'}, callback=self.parse_page)
        else:
            indexpage = response.xpath('//div[@class="btn-group btn-group-paging"]//a[@class="btn wide"][2]/@href').extract_first()
            url = 'https://www.ptt.cc/' + indexpage
            yield scrapy.Request(url=url, cookies={'over18': '1'}, callback=self.parse_page)

    def parse_page(self, response):
        articles = response.xpath('//div[@class="title"]//a/@href').extract()
        for a in articles:
            url = 'https://www.ptt.cc' + a
            # if url in self.olds:
            
            if self.ptt_content.count_documents({"page_url":url }, limit=1):
                print('=' * 100)
                continue
            else:
                # print(url)
                yield scrapy.Request(url=url, cookies={'over18': '1'}, callback=self.parse_content)
   
    def parse_content(self, response):

        text = response.xpath('//div[@class="bbs-screen bbs-content"]/text()').extract()
        info = response.xpath('//div[@id="main-content"]//div[@class="article-metaline"]//span[@class="article-meta-value"]/text()').extract()
        pushes = response.xpath('//div[@class="push"]//span[@class="f3 push-content"]/text()').extract()
        post_time = response.xpath('//div[@class="article-metaline"]//span[@class="article-meta-value"]/text()').extract()
        
        if post_time:
            post_time = post_time[-1]
        else:
            post_time = ''

        if info:
            if len(info) == 1:
                author = info[0]
                title = ''
            else:
                author = info[0]
                title = info[1]
        else:
            author = ''
            title = ''
            
        if text:
            taipei = timezone('Asia/Taipei')
            taipei_time = datetime.now(taipei)
            
            ptt_item = PttProjectItem()
            ptt_item['title'] = title
            ptt_item['page_url'] = response.url
            ptt_item['author'] = author
            ptt_item['text'] = text
            ptt_item['push'] = pushes
            ptt_item['board'] = response.url.split('/')[4]
            ptt_item['post_time'] = post_time
            ptt_item['crawl_time'] = taipei_time.strftime('%a %b %e %H:%M:%S %Y')
            print(f"{Fore.CYAN}{post_time} {Fore.YELLOW}{response.url.split('/')[4]}  {Fore.GREEN}{title}{Style.RESET_ALL}")     
            yield ptt_item
        else:
            print(f"{Fore.RED}{response.url}{Style.RESET_ALL}")