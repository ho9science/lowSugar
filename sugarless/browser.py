from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas
import io

browser = webdriver.Firefox()

url = "https://finance.naver.com/sise/sise_rise.nhn"
browser.get(url)

browser.implicitly_wait(3)

option4 = browser.find_element_by_id('option4').click()
browser.find_element_by_id('option22').click()
browser.find_element_by_id('option17').click()
browser.find_element_by_id('option24').click()

browser.find_element_by_id('option12').click()
browser.find_element_by_id('option2').click()
browser.find_element_by_id('option8').click()
browser.find_element_by_id('option14').click()
browser.find_element_by_id('option20').click()

browser.find_element_by_xpath('//a[@href="javascript:fieldSubmit()"]').click()

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

datas = []
for row in rows:
	cols = row.find_all('td')
	if len(cols) > 1:
		tl = [col.text.strip() for col in cols]
		datas.append(tl)

with open('test123.csv', 'w', newline='') as f:
	wr = csv.writer(f, quoting=csv.QUOTE_ALL)
	wr. writerow(datas)