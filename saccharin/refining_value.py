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
	find_diff(df)
	save_stockcode(df)
	del df["name"]
	result = df.to_json(orient="records")
	return json.loads(result)

def store_data(sugars):
	dynamodb = boto3.resource('dynamodb')

	table = dynamodb.Table('stock')

	print(table.creation_date_time)
	start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	print("start: ", start_time)
	with table.batch_writer() as batch:
		for sugar in sugars:

			batch.put_item(
			Item=sugar
			)
			
	endtime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	print("end: ", endtime)

def save_stockcode(df):
	df = df.loc[:,['id','name']]
	df = df.set_index('id')
	data = df.to_dict("index")
	with open('stockcode.json', 'w') as outfile:
		json.dump(data, outfile, ensure_ascii=False)

def find_diff(df):
	try:
		df2 = pd.read_json("stockcode.json", orient='index')
		deletedCode = df.index.difference(df2.index)
		addedCode = df2.index.difference(df.index)

		print('--- 삭제 목록 ---')
		print('\n'.join(map(str, deletedCode)))
		print('--- 추가 목록 ---')
		print('\n'.join(map(str, addedCode)))

	except ValueError:
		print("not find stockcode")

if __name__ == '__main__':
	getDailyData()
	data = refine_data()
	store_data(data)
