import scrapy
from lowerSugar.items import LowersugarItem
class LowersugarSpider(scrapy.Spider):

	with open('realcodelist.txt', 'r') as f:
		var = f.readlines()
	f.close
	#http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd=005930&fin_typ=0&freq_typ=A&extY=1&extQ=1
	url = []
	for nandc in var:
		value = nandc.split(" ")
		url.append('http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd='+value[0]+'&fin_typ=0&freq_typ=A&extY=1&extQ=1')
	
	name = "lowerSugar"
	start_urls = url

	#def start_requests(self):
	#    yield scrapy.Request('http://www.example.com/1.html', self.parse) 

	def parse(self, response):
		year = '4' #2016
		items = response.xpath('//tr')
		var = 0
		refine = 0
		my_item = LowersugarItem()
		for item in items:
			if var > 1 :
				data = item.xpath('td['+year+']/span/text()').extract()
				temp = "".join(str(x) for x in data)
				temp = temp.replace(",","")
				try :
					refinedata = float(temp)
				except :
					refinedata = float('NaN')
			if var == 0 :
				codeUrl = response.url
				code = codeUrl.split('cmp_cd',7)
				real = code[1].split('&')
				corp = real[0].replace("=","")
				my_item['code'] = corp.rstrip('%0A')
			elif var == 2:
				my_item['sales'] = refinedata
			elif var == 3:
				my_item['businessprofits'] = refinedata
			elif var == 4:
				my_item['continuing'] = refinedata
			elif var == 5:
				my_item['netincome'] = refinedata
			elif var == 6:
				my_item['netincomeruling'] = refinedata
			elif var == 7:
				my_item['netincomenon'] = refinedata
			elif var == 8:
				my_item['asset'] = refinedata
			elif var == 9:
				my_item['liabilities'] = refinedata
			elif var == 10:
				my_item['totalequities'] = refinedata
			elif var == 11:
				my_item['totalequitiesruling'] = refinedata
			elif var == 12:
				my_item['totalequitiesnon'] = refinedata
			elif var == 13:
				my_item['eqities'] = refinedata
			elif var == 14:
				my_item['cashbusiness'] = refinedata
			elif var == 15:
				my_item['cashinvestment'] = refinedata
			elif var == 16:
				my_item['cashfinance'] = refinedata
			elif var == 17:
				my_item['capex'] = refinedata
			elif var == 18:
				my_item['fcf'] = refinedata
			elif var == 19:
				my_item['ibl'] = refinedata
			elif var == 20:
				my_item['roop'] = refinedata
			elif var == 21:
				my_item['netprofitmargin'] = refinedata
			elif var == 22:
				my_item['roe'] = refinedata
			elif var == 23:
				my_item['roa'] = refinedata
			elif var == 24:
				my_item['debtratio'] = refinedata
			elif var == 25:
				my_item['err'] = refinedata
			elif var == 26:
				my_item['eps'] = refinedata
			elif var == 27:
				my_item['per'] = refinedata
			elif var == 28:
				my_item['bps'] = refinedata
			elif var == 29:
				my_item['pbr'] = refinedata
			elif var == 30:
				my_item['dps'] = refinedata
			elif var == 31:
				my_item['rcdp'] = refinedata
			elif var == 32:
				my_item['cdr'] = refinedata
			elif var == 33:
				my_item['stock'] = refinedata
			var=var+1;
		yield my_item