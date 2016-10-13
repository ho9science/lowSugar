# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import log

class LowersugarPipeline(object):

	collection_name = 'scrapy_items7'

	def __init__(self, mongo_uri, mongo_db):
		self.mongo_uri = mongo_uri
		self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mongo_uri=crawler.settings.get('mongodb://localhost:27017'),
			mongo_db = crawler.settings.get('mongo_database', "mongo_database")
		)

	def open_spider(self, spider):
		self.client = pymongo.MongoClient(self.mongo_uri)
		self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
		self.client.close()

	def process_item(self, item, spider):
		valid = True
		for data in item:
			if not data:
				valid = False
				log.msg("add mongo db error", level=log.DEBUG, spider=spider)
		if valid:
			self.db[self.collection_name].insert(dict(item))
			log.msg("add mongo db success", level=log.DEBUG, spider=spider)
		return item
