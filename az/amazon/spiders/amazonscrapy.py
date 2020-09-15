# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonScrapyItem
from datetime import datetime ,timezone
class AmazonscrapySpider(scrapy.Spider):
    name = 'amazonscrapy'
    #allowed_domains = ['www.amazon.com']
    start_urls = []

    #'https://www.amazon.com/s?k=apple&i=electronics&ref=nb_sb_noss_2'
    def __init__(self, url,start_product_from,end_product_to,images,product_description,limit_pages,reviews, *args, **kwargs):
        super(AmazonscrapySpider, self).__init__(*args, **kwargs) # <- important
        self.start_urls.append(url)
        self.start_product_from = start_product_from
        self.end_product_to = end_product_to
        self.limit_pages = limit_pages
        self.reviews = int(reviews) # 0 - no reviews , 1 - scrape reviews 
        self.images = int(images)
        self.product_description = int(product_description)

       
       

    def parse(self, response):
        for post in response.css('.a-section .a-spacing-none h2')[int(self.start_product_from) if self.start_product_from!='' else 0:int(self.end_product_to) if self.end_product_to!='' else len(response.css('.a-section .a-spacing-none h2')) ] :
            yield scrapy.Request(url = response.urljoin(post.css('a::attr(href)').get()) , callback = self.parse_product)
      
        product_nextpage = response.css('.a-pagination .a-last a::attr(href)').get()
        if product_nextpage is not None:
            if int(response.css('.a-pagination li.a-selected a::text').get()) < int(self.limit_pages):
                product_nextpage_url = response.urljoin(product_nextpage)
                yield scrapy.Request(product_nextpage_url,callback=self.parse)
       

    
    def parse_product(self, response):
        item = AmazonScrapyItem()
        item['product_name'] = response.xpath('//*[@id="productTitle"]/text()').get()
        item['price'] = response.xpath('//*[@id="priceblock_ourprice"]/text()').get()
        item['price_saving'] =  response.xpath('//*[@id="regularprice_savings"]/text()').get()
        item['list_price'] = response.css('.priceBlockStrikePriceString::text').get()
        item['size'] = response.xpath('//*[@id="variation_size_name"]/div/span/text()').get()
        item['url'] = response.request.url
        if self.images == 1:
            item['images'] =  response.css('.item .a-button-text img::attr(src)').getall()
        item['avg_rating'] = float(response.css('.averageStarRating span::text').get()[0:3]) 

        if self.product_description == 1:
            item['product_description'] = response.xpath('//*[@id="productDescription"]/p/text()').get()
        
        item['best_seller'] = response.css('#zeitgeistBadge_feature_div .badge-link i::text').get()
        item['best_seller_category'] = response.css('#zeitgeistBadge_feature_div .badge-link .cat-name span::text').get()

        item['product_information'] = []
        for x in response.css('.prodDetTable'):
            item['product_information'].append(dict(zip(x.css('th *::text').getall() ,x.css('td *::text').getall() )))

        r_url = response.xpath('//*[@id="reviews-medley-footer"]/div[2]/a/@href').get()
        
        item['reviews'] = []
        if r_url is not None and self.reviews == 1 :
            all_review_url = response.urljoin(r_url)
            
            yield scrapy.Request(all_review_url,callback=self.parse_review , meta={'item': item })
        else:
            yield item

       

        
        #yield{'product_name':product_name ,'price':price ,  'price_saving': price_saving,'list_price':list_price , 'images': images , 'url': url , 'size':size ,'avg_rating':avg_rating 
        #,'product_information':product_information , 'best_seller':best_seller , 'best_seller_category': best_seller_category}
    
    def parse_review(self,response):
        item = response.meta['item']
        for x in response.css('#cm_cr-review_list .review .celwidget'):
            single_review = {}
            single_review['review_title'] = x.css('.review-title span::text').get()
            single_review['review_body'] = " ".join(x.css('.review-text  span::text').extract())
            single_review['review'] = int(x.css('.review-rating span::text').get()[0])
            single_review['review_date'] = str(datetime.strptime(x.css('.review-date::text').get().replace('Reviewed in the United States on ',''), '%B %d, %Y').date())
            single_review['review_time'] = str(datetime.strptime(x.css('.review-date::text').get().replace('Reviewed in the United States on ',''), '%B %d, %Y').time())
            single_review['review_by'] = x.css('.a-profile-name::text').get()
            single_review['review_url'] = response.request.url
            if x.css('.cr-vote-text::text').get() is not None:
                single_review['helpful_vote'] = x.css('.cr-vote-text::text').get().replace('people found this helpful', '')
            else:
                single_review['helpful_vote'] = 0

            item['reviews'].append(single_review)
        

        next_page = response.xpath('//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a/@href').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url,callback=self.parse_review , meta={'item': item })    
        else:
            yield item
       

