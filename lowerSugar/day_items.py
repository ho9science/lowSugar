# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SugarDayItem(scrapy.Item):
	date = scrapy.Field()
	closing = scrapy.Field()
	opening = scrapy.Field()
	high = scrapy.Field()
	lower = scrapy.Field()
	volume = scrapy.Field()
	