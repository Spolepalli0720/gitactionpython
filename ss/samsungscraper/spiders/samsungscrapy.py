# -*- coding: utf-8 -*-
import scrapy
from ..items import SamsungscraperItem
from datetime import datetime ,timezone
import json
import os

from pymongo import MongoClient

client = MongoClient(os.environ.get('SCRAPERS_DB_URL', "mongodb://localhost:27017"))

class SamsungscrapySpider(scrapy.Spider):
    name = 'samsungscrapy'
    #allowed_domains = ['www.samsung.com']
    start_urls = []


    def __init__(self, keyword,reviews,pages, *args, **kwargs):
        super(SamsungscrapySpider, self).__init__(*args, **kwargs) # <- important
        url = 'https://www.samsung.com/us/api/es_search_global/global/result.json?listType=g&searchTerm='+keyword+'&from=0&sort=relevance'
        self.start_urls.append(url)
        self.keyword = keyword
        self.reviews = int(reviews)
        
        self.pages = pages
            
        self.items = SamsungscraperItem()

    def parse(self, response):
        jsonresponse = json.loads(response.text)
        if self.pages != '':
            page_count = int(self.pages)
        else:
            page_count = int(jsonresponse['page']['totalPages']) +1
        for x in range(page_count):
            from_count = x * 30
            page_url = 'https://www.samsung.com/us/api/es_search_global/global/result.json?listType=g&searchTerm='+self.keyword+'&from='+str(from_count)+'&sort=relevance'
            yield scrapy.Request(page_url,callback=self.parse_main )

    def parse_main(self, response):
        jsonresponse = json.loads(response.text)
        for x in range(30):
            self.items['product_code'] = jsonresponse['results'][x]['attributes']['ModelCode'][0]
            product_info = jsonresponse['results'][x]['attributes']
            product_info.pop("B2B.LinkUrl", None)
            product_info.pop("Support.LinkUrl", None)
            self.items['product_info'] = product_info
            self.items['reviews'] = []
            self.items['review_url'] = 'https://api.bazaarvoice.com/data/batch.json?passkey=cazyYOSgdvV4AJhcGd18eBaG5v9hyy1bBvfq1WD7wlGSQ&apiversion=5.5&displaycode=20545-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A'+self.items['product_code']+'&filter.q0=contentlocale%3Aeq%3Aen*%2Cen_US&sort.q0=helpfulness%3Adesc%2Ctotalpositivefeedbackcount%3Adesc&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&limit.q0=100&offset.q0=0&limit_comments.q0=20'
            yield self.items
            
            if self.reviews == 1:
                yield scrapy.Request(self.items['review_url'],callback=self.parse_review )
            #print(jsonresponse['results'][x]['attributes']['LinkUrl'][0])

    def parse_review(self, response):
        review_url = response.request.url
        jsonresponse_review = json.loads(response.text)
        product_code = review_url.split('q0=productid%3Aeq%3A')[1].split('&')[0]
        product_review_count = int(jsonresponse_review['BatchedResults']['q0']['TotalResults'])
        review_limit = 100
        for y in jsonresponse_review['BatchedResults']['q0']['Results']:
            client.scraper.samsung_data.update_one({'product_code': product_code},{'$push': {'reviews': y.copy()}}, upsert=True)
        if product_review_count / review_limit > 1:
            for i in range(int(product_review_count / review_limit)+1):
                offset = i * 100
                review_api = 'https://api.bazaarvoice.com/data/batch.json?passkey=cazyYOSgdvV4AJhcGd18eBaG5v9hyy1bBvfq1WD7wlGSQ&apiversion=5.5&displaycode=20545-en_us&resource.q0=reviews&filter.q0=isratingsonly%3Aeq%3Afalse&filter.q0=productid%3Aeq%3A'+product_code+'&filter.q0=contentlocale%3Aeq%3Aen*%2Cen_US&sort.q0=helpfulness%3Adesc%2Ctotalpositivefeedbackcount%3Adesc&stats.q0=reviews&filteredstats.q0=reviews&include.q0=authors%2Cproducts%2Ccomments&filter_reviews.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&filter_comments.q0=contentlocale%3Aeq%3Aen*%2Cen_US&limit.q0=100&offset.q0='+str(offset)+'&limit_comments.q0=20'
                yield scrapy.Request(review_api,callback=self.parse_allreviews )
            

    def parse_allreviews(self, response):
        review_url = response.request.url
        jsonresponse_review = json.loads(response.text)
        product_code = review_url.split('q0=productid%3Aeq%3A')[1].split('&')[0]
        for y in jsonresponse_review['BatchedResults']['q0']['Results']:
            client.scraper.samsung_data.update_one({'product_code': product_code},{'$push': {'reviews': y.copy()}}, upsert=True)
        


