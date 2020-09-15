# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WalmartItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    product_information = scrapy.Field()
    product_description = scrapy.Field()
    product_specifications = scrapy.Field()
    images = scrapy.Field()
    reviews = scrapy.Field()
    review_url = scrapy.Field()
