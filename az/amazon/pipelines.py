# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os

class AmazonPipeline:

    DB_URI = os.environ.get('SCRAPERS_DB_URL', "mongodb://localhost:27017")

    def __init__(self):
        self.conn = pymongo.MongoClient(self.DB_URI)
        db = self.conn['scraper']
        self.collection = db['amazon_data']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
