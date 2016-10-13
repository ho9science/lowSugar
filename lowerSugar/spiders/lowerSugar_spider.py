import scrapy
from lowerSugar.items import LowersugarItem
class LowersugarSpider(scrapy.Spider):
	name = "lowerSugar"
	url = 'http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=005930&fin_typ=0&freq_typ=A&extY=1&extQ=1'
	start_urls = [
		#'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd=012320&target=finsum_more',
		url,
	]
	global corp
	code = url.split('cmp_cd',7)
	real = code[1].split('&')
	corp = real[0].replace("=","")
	
	#def start_requests(self):
    #    yield scrapy.Request('http://www.example.com/1.html', self.parse)
     
	def parse(self, response):
		year = '3' #2015
		items = response.xpath('//tr')
		var = 0
		my_item = LowersugarItem()
		for item in items:
			if var == 0 :
				my_item['code'] = corp;
			elif var == 2:
				my_item['sales'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 3:
				my_item['businessprofits'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 4:
				my_item['continuing'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 5:
				my_item['netincome'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 6:
				my_item['netincomeruling'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 7:
				my_item['netincomenon'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 8:
				my_item['asset'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 9:
				my_item['liabilities'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 10:
				my_item['totalequities'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 11:
				my_item['totalequitiesruling'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 12:
				my_item['totalequitiesnon'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 13:
				my_item['cashbusiness'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 14:
				my_item['cashinvestment'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 15:
				my_item['cashfinance'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 16:
				my_item['capex'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 17:
				my_item['fcf'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 18:
				my_item['ibl'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 19:
				my_item['roop'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 20:
				my_item['netprofitmargin'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 21:
				my_item['roe'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 22:
				my_item['roa'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 23:
				my_item['debtratio'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 24:
				my_item['err'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 25:
				my_item['eps'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 26:
				my_item['per'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 27:
				my_item['bps'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 28:
				my_item['pbr'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 29:
				my_item['dps'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 30:
				my_item['rcdp'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 31:
				my_item['cdr'] = item.xpath('td['+year+']/span/text()').extract()
			elif var == 32:
				my_item['stock'] = item.xpath('td['+year+']/span/text()').extract()
			var=var+1;
		yield my_item
			