# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PttProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    page_url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    text = scrapy.Field()
    post_time = scrapy.Field()
    crawl_time = scrapy.Field()
    board = scrapy.Field()
    push = scrapy.Field()