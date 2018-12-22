import scrapy
from lowerSugar.day_items import SugarDayItem
class LowersugarSpider(scrapy.Spider):

	# with open('realcodelist.txt', 'r') as f:
	# 	var = f.readlines()
	# f.close
	#http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=005930&fin_typ=0&freq_typ=A&extY=1&extQ=1
	url = []
	url.append('https://finance.naver.com/item/sise_day.nhn?code=000250&page=1')

	# for nandc in var:
	# 	value = nandc.split(" ")
	# 	url.append('https://finance.naver.com/item/sise_day.nhn?code=000250&page=1')
	
	name = "sugar_day"
	start_urls = url

	#def start_requests(self):
	#    yield scrapy.Request('http://www.example.com/1.html', self.parse) 

	def normalize_num(self, item, my_item):
		data = item.xpath('td[contains(@class, "num")]/span/text()').extract()
		var = 0
		for value in data:
			temp = "".join(value)
			temp = temp.replace(",","")
			try :
				refinedata = float(temp)
			except :
				refinedata = float('NaN')
			if var == 0:
				my_item['closing'] = refinedata
			elif var == 2:
				my_item['opening'] = refinedata
			elif var == 3:
				my_item['high'] = refinedata
			elif var == 4:
				my_item['lower'] = refinedata
			elif var == 5:
				my_item['volume'] = refinedata
			var+=1
		
		return my_item

	def normalize_date(self, data):
		print(data)
		temp = "".join(str(x) for x in data)
		return temp

	def parse(self, response):
		items = response.xpath('//tr')
		my_item = SugarDayItem()
		var = 0
		print(len(items))
		for item in items:
			data = item.xpath('td[contains(@align, "center")]/span/text()').extract()
			if not data:
				continue	
			my_item = self.normalize_num(item, my_item)
			my_item['date'] = self.normalize_date(data)
			yield my_item
