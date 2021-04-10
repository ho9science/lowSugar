import pandas as pd
import xml.etree.ElementTree as ET

import boto3
import json
import time
from datetime import datetime
import sys
import requests

def get_code_list():
	with open("stockcode.json") as code:
		return json.load(code)

def request_from_source(code):
	url = ''+code
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}

	try:
		r = requests.get(url, headers=headers)
	except requests.exceptions.Timeout:
		print("timeout : ", code)
	except requests.exceptions.TooManyRedirects:
		print("too many redirect : ", code)
	except requests.exceptions.RequestException as e:
		raise SystemExit(e)

	xmlp = ET.XMLParser(encoding="utf-8")
	root = ET.fromstring(r.text, parser=xmlp)
	data = [item.attrib.get('data').split('|') for item in root[0]]
	index  = ['date', 'open', 'high', 'low', 'close', 'volume']

	df = pd.DataFrame(data, columns=index)
	df['id'] = code
	df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').astype(str)

	return df

def store_data(df):
	result = df.to_json(orient="records")
	sugars = json.loads(result)

	dynamodb = boto3.resource('dynamodb')

	table = dynamodb.Table('stock')

	start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	print("start : ", start_time)
	with table.batch_writer() as batch:
		for sugar in sugars:

			batch.put_item(
			Item=sugar
			)
			
	endtime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
	print("end : ", endtime)


if __name__ == '__main__':
	data = get_code_list()
	total = 0
	for code in data:
		total+=1
		print("preparing ", total, " : ", code)

		df = request_from_source(code)
		store_data(df)
		time.sleep(2)
