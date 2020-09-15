# -*- coding: utf-8 -*-
import scrapy
from ..items import WalmartItem
from datetime import datetime ,timezone


class WalmartscrapySpider(scrapy.Spider):
    name = 'walmartscrapy'
    #allowed_domains = ['www.walmart.com/search/?cat_id=0&facet=brand%3ASamsung']
    start_urls = []
    

    def __init__(self, url,reviews,limit_pages,images,product_specifications,product_description,product_information, *args, **kwargs):
        super(WalmartscrapySpider, self).__init__(*args, **kwargs) # <- important
        self.start_urls.append(url)
        self.reviews = int(reviews)
        self.request_url = url
        self.url_counter = 2
        self.limit_pages = int(limit_pages)
        self.images = int(images)
        self.product_specifications = int(product_specifications)
        self.product_description = int(product_description)
        self.product_information = int(product_information)
        self.items = WalmartItem()



    def parse(self, response):
        urls = response.css(".search-result-product-title a::attr(href)").getall()
        
        if len(urls)>0:
            for url in urls:
                yield scrapy.Request(response.urljoin(url),callback=self.parse_product)
            
            #  change this block of code , get url from js
            while self.url_counter < self.limit_pages:
                product_nextpage_url = self.request_url +'&page='+str(self.url_counter)
                yield scrapy.Request(product_nextpage_url,callback=self.parse)
                self.url_counter +=1

        

        

    
    def parse_product(self,response):
        self.items = WalmartItem()
        self.items['product_name'] = response.css('h1.prod-ProductTitle::text').get()
        self.items['price'] = response.css('span#price .price span::text').get()
        self.items['old_price'] = response.css('.price-old .price span::text').get()
        
        if self.product_information == 1:
            self.items['product_information'] = response.css('.about-product-description::text').get()
        
        if self.product_description  == 1:
            self.items['product_description'] = response.css('.about-product-description li::text').getall()

        if self.product_specifications == 1:
            self.items['product_specifications'] = []
            for x in response.css('.product-specification-table'):
                self.items['product_specifications'].append(dict(zip(x.css('td::text').getall() ,x.css('td div::text').getall() )))

        if self.images == 1:
            self.items['images'] = response.css('.hover-zoom-hero-image::attr(src)').get()

        self.items['reviews'] = []
        r_url = response.css('.ReviewBtn-container::attr(href)').get()
        if r_url is not None and self.reviews == 1:
            all_review_url = response.urljoin(r_url)
            yield scrapy.Request(all_review_url,callback=self.parse_reviewpages , meta={'item': self.items,'review_url':all_review_url })
        else:
            yield self.items

    
    def parse_reviewpages(self,response):
        item = response.meta['item']
        review_url = response.meta['review_url']
        

        for x in response.css('.customer-review-body'):
            single_review = {}
            single_review['review'] = int(float((x.css('.review-star-rating .average-rating .seo-avg-rating::text').get())))
            single_review['review_title'] = x.css('.review-heading h3::text').get()
            single_review['review_body'] =" ".join(x.css('.review-body p::text').extract())
            single_review['review_date'] = str(datetime.strptime(x.css('.review-footer-submissionTime::attr(content)').get(), '%B %d, %Y').date())
            single_review['review_time'] = str(datetime.strptime(x.css('.review-footer-submissionTime::attr(content)').get(), '%B %d, %Y').time())
            single_review['review_by'] = x.css('.review-footer-userNickname::text').get()
            single_review['review_url'] = response.request.url
            item['reviews'].append(single_review.copy())

        next_page = response.xpath('//*[@class="paginator-list"]/li[@class="active"]/following-sibling::li[1]/button/text()').get()
        if next_page is not None:
            next_page_url = review_url + '?page='+str(next_page)
            yield response.follow(next_page_url,callback=self.parse_reviewpages , meta={'item': item , 'review_url':review_url}) 
        else:
            yield item

      
        
        
