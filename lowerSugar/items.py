# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LowersugarItem(scrapy.Item):
	code = scrapy.Field()
	sales = scrapy.Field()
	businessprofits = scrapy.Field()
	continuing = scrapy.Field()
	netincome = scrapy.Field()
	netincomeruling = scrapy.Field()
	netincomenon = scrapy.Field()
	asset = scrapy.Field()
	liabilities = scrapy.Field()
	totalequities = scrapy.Field()
	totalequitiesruling = scrapy.Field()
	totalequitiesnon = scrapy.Field()
	eqities = scrapy.Field()
	cashbusiness = scrapy.Field()
	cashinvestment = scrapy.Field()
	cashfinance = scrapy.Field()
	capex = scrapy.Field()
	fcf = scrapy.Field()
	ibl = scrapy.Field()
	roop = scrapy.Field()
	netprofitmargin = scrapy.Field()
	roe = scrapy.Field()
	roa = scrapy.Field()
	debtratio = scrapy.Field()
	err = scrapy.Field()
	eps = scrapy.Field()
	per = scrapy.Field()
	bps = scrapy.Field()
	pbr = scrapy.Field()
	dps = scrapy.Field()
	rcdp = scrapy.Field()
	cdr = scrapy.Field()
	stock = scrapy.Field()
	#column = scrapy.Field()
	#y2013 = scrapy.Field()
	#y2014 = scrapy.Field()
	#y2015 = scrapy.Field()
	#y2016 = scrapy.Field()