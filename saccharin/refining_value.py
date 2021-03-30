import pandas as pd
import glob
import os
import json
import boto3
from datetime import datetime, timedelta
import selenium
from selenium import webdriver
import time

import pandas as pd 

def getDailyData():
	url = ""
	driver = webdriver.Chrome('../driver/chromedriver')
	candidate = []
	driver.implicitly_wait(time_to_wait=5)

	driver.get(url=url)
	driver.find_element_by_link_text("주식").click()
	driver.find_element_by_link_text("종목시세").click()
	driver.find_element_by_link_text("전종목 시세").click()
	time.sleep(5)
	driver.find_element_by_class_name('CI-MDI-UNIT-DOWNLOAD').click()
	div = driver.find_element_by_xpath("//div[@data-type='csv']")
	div.find_element_by_tag_name('a').click()
	time.sleep(5)
	driver.close()

def refine_data():
	list_of_files = glob.glob('/Users/henry/Downloads/*.csv')
	latest_file = max(list_of_files, key=os.path.getctime)
	df = pd.read_csv(latest_file, encoding="cp949")
	df.drop(df.columns[[2,3,5,6,11,12,13]], axis=1, inplace=True)
	df.columns = ['id', 'name', 'close', 'open', 'high', 'low', 'volume']
	df['date'] = datetime.today().strftime('%Y-%m-%d')

	result = df.to_json(orient="records")
	return json.loads(result)

def store_data(sugars):
	dynamodb = boto3.resource('dynamodb')

	table = dynamodb.Table('stock')

	print(table.creation_date_time)

	with table.batch_writer() as batch:
		for sugar in sugars:

			batch.put_item(
			Item=sugar
			)

if __name__ == '__main__':
	getDailyData()
	data = refine_data()
	store_data(data)
