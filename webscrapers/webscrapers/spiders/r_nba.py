# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
import time 

class RNbaSpider(scrapy.Spider):
    name = 'r-nba'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.reddit.com/r/nba/top/',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']
        for i in range(5):
            driver.execute_script("window.scrollBy(0, 1000);")
            time.sleep(3)
        
        posts = response.xpath("//div[@data-testid='post-container']")
        for post in posts:
            flair = post.xpath(".//div[3]/div[2]/div[@class='_2xu1HuBz1Yx6SP10AGVx_I']/div[2]/a/div/span/text()").get()
            if flair == "Highlight":
                yield {
                    'title': post.xpath(".//div[3]/div[2]/div[1]/a/div/h3/text()").get(),
                    'link': post.xpath("div[3]/div[3]/a/@href").get(),
                    'views': post.xpath("div[2]/div/div/text()").get()
                }
        driver.close()    
                
