# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class  AmazonRevItem(scrapy.Item):
    product_name = scrapy.Field()
    review = scrapy.Field()

class AmazonScrapyItem(scrapy.Item):
    product_name = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    price_saving = scrapy.Field()
    list_price  = scrapy.Field()
    size = scrapy.Field()
    images = scrapy.Field()
    avg_rating = scrapy.Field()
    product_description = scrapy.Field()
    best_seller = scrapy.Field() 
    best_seller_category = scrapy.Field()
    product_information = scrapy.Field()
    review_url = scrapy.Field()
    reviews = scrapy.Field()