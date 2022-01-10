# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class Hot100Spider(scrapy.Spider):
    name = 'hot100'

    def remove_characters(self, value):
        return value.strip('\n')

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.billboard.com/charts/hot-100/',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        songs = response.xpath("//div[@class='o-chart-results-list-row-container']")
        for song in songs:
            yield {
                'Song': self.remove_characters(song.xpath(".//ul/li[4]/ul/li/h3/text()").get()),
                'Artists': self.remove_characters(song.xpath(".//ul/li[4]/ul/li[1]/span[1]/text()").get()),
                'Ranking': self.remove_characters(song.xpath(".//ul/li[1]/span[1]/text()").get()),
                'Weeks on Chart': self.remove_characters(song.xpath(".//ul/li[4]/ul/li[6]/span/text()").get())
            }

