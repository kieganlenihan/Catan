#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 22:04:46 2020

@author: kieganlenihan
"""

import scrapy

class RedditbotSpider(scrapy.Spider):
    name = 'redditbot'
    allowed_domains = ['www.reddit.com/r/gameofthrones/']
    start_urls = ['http://www.reddit.com/r/gameofthrones//']
    
    def parse(self, response):
        # Extracting the content using css selectors
        titles = response.css('.title.may-blank::text').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
        comments = response.css('.comments::text').extract()
       
        # Give the extracted content row wise
        for item in zip(titles,votes,times,comments):
            #create a dictionary to store the scraped info
            scraped_info = {
                'title' : item[0],
                'vote' : item[1],
                'created_at' : item[2],
                'comments' : item[3],
            }

            #yield or give the scraped info to scrapy
            yield scraped_info