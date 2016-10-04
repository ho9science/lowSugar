import scrapy
from lowerSugar.items import LowersugarItem

class LowersugarSpider(scrapy.Spider):
	name = "lowerSugar"
	start_urls = [
		#'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=012320&target=finsum_more',
		'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=005930&fin_typ=0&freq_typ=A&extY=1&extQ=1',
	]

	def parse(self, response):
		#filename = 'jusik-' + response.url.split("/")[-2] + '.html'
		#with open(filename, 'wb') as f:
		#	f.write(response.body)
		
		items = response.xpath('//td')
		var = 0
		for item in items:
			my_item = LowersugarItem()
			my_item['text'] = item.xpath('//span/text()').extract()
			#var = item.xpath('./text()').extract()
			var+=1
			print(my_item['text']);
		print(var)
			