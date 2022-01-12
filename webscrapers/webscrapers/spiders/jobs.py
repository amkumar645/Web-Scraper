# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.keys import Keys
import time


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    count = 0

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.indeed.com/',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        if self.count == 0:
            driver = response.meta['driver']
            job_input = driver.find_element_by_xpath("//input[@placeholder='Job title, keywords, or company']")
            # Change this to whatever job title you want
            job_input.send_keys("Software Intern")
            location_input = driver.find_element_by_xpath("//input[@id='text-input-where']")
            # Change this to KEYS.CONTROL + "a" if on Windows
            location_input.send_keys(Keys.COMMAND + "a")
            location_input.send_keys(Keys.DELETE)
            # Change this to whatever location you want
            location_input.send_keys("Boston, MA")
            location_input.send_keys(Keys.ENTER)
            self.count += 1
            html = driver.page_source
            response = Selector(text=html)
            
        jobs = response.xpath("//div[@id='mosaic-provider-jobcards']/a")
        for job in jobs:
            job_desc = job.xpath(".//div[1]/div[1]/div[1]/div[1]")
            job_url = job.xpath(".//@href").get()
            yield {

                'Position': job_desc.xpath(".//table/tbody/tr/td/div[1]/h2/span/text()").get(),
                'Company': job_desc.xpath(".//table/tbody/tr/td/div[2]/pre/span[1]/text()").get(),
                'Location': job_desc.xpath(".//table/tbody/tr/td/div[2]/pre/div/text()[1]").get(),
                'Application Link': f"https://indeed.com{job_url}",
            }
        next_page = response.xpath("//a[@aria-label='Next']/@href").get()
        if next_page:
            absolute_url = f"https://indeed.com{next_page}"
            yield SeleniumRequest (
                url = absolute_url,
                wait_time=3,
                callback=self.parse
            )
        