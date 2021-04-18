import pandas as pd
import requests
import json
import re
import boto3
from datetime import datetime
import time

def check_value(value):
    regex = '(\d{4}).(03|06|09|12).(\d{2})'
    return re.search(regex, str(value)).group(0)

def request_single_account(payload):
    r = requests.get('https://opendart.fss.or.kr/api/fnlttSinglAcnt.json', params=payload)
    data_json = json.loads(r.text)
    if data_json.get('status') == '013':
        print(data_json.get('message'))
        return ''
    data = data_json.get('list')
    dart = {}
    for item in data:
        if item.get('fs_div') == 'CFS':
            account_nm = item.get('account_nm')
            thstrm_amount= item.get('thstrm_amount')
            stock_code = item.get('stock_code')
            thstrm_dt = item.get('thstrm_dt')
            dart[account_nm] = thstrm_amount.replace(',', '')
            dart['stock_code'] = stock_code
            dart['thstrm_dt'] = thstrm_dt
    if not dart:
        return dart
    dart['thstrm_dt'] = check_value(dart.get('thstrm_dt'))
    
    df = pd.json_normalize(dart)
   
    result = df.to_json(orient="records")
    return json.loads(result)

def set_payload(corp_code):
    bsns_year = '2015'
    reprt_code = '11011'# 1분기: 11013, 2분기 : 11012, 3분기: 11014, 사업보고서: 11011
    fs_div = 'CFS'
    crtfc_key = ''
    return {'crtfc_key': crtfc_key, 'corp_code': corp_code, 'bsns_year':bsns_year, 'reprt_code': reprt_code, 'fs_div':fs_div}

def store_data(sugars):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('financial_data')

    with table.batch_writer() as batch:
        for sugar in sugars:
            batch.put_item(
            Item=sugar
            )

def view_data(data):
    print(data)
    
def get_corp_code():
    with open('corp_code.json') as r:
        return json.load(r)

def do_work():
    corp_list = get_corp_code()
    start_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print("start: ", start_time)
    for item in corp_list:
        corp_code = item.get('corp_code')
        print("start : ", corp_code)
        payload = set_payload(corp_code)
        data = request_single_account(payload)
        store_data(data)
        time.sleep(0.7)

    endtime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print("end: ", endtime)


if __name__ == '__main__':
    do_work()