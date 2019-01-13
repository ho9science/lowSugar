from selenium import webdriver
from bs4 import BeautifulSoup
import time

#need to getcko driver
browser = webdriver.Firefox()

url = "url"
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
table = soup.find('table', attrs={'class':'type_2'})

table_body = table.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
	cols = row.find_all('td')
	# print(cols)
