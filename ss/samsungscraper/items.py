# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SamsungscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    reviews = scrapy.Field()
    product_info = scrapy.Field()
    product_code = scrapy.Field()
    review_url = scrapy.Field()
