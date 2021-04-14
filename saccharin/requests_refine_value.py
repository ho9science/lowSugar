import pandas as pd
import io
import requests as r
import json
import boto3
import pandas as pd
from datetime import datetime


def get_daily_data():
    generate_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    today = datetime.today().strftime('%Y%m%d')
    otp_data = {
        'mktId': 'ALL',
        'trdDd': "20210409",
        'share': 1,
        'money': 1,
        'csvxls_isNo' : False,
        'name': 'fileDown',
        'url' : 'dbms/MDC/STAT/standard/MDCSTAT01501'
    }

    otp = r.post(generate_otp_url, data = otp_data)
    code = otp.content

    down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
    referer = {'referer': generate_otp_url,
              'user-agent': 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    data = {'code': code}
    down_sector_ks = r.post(down_url, data=data, headers = referer)
    decoded_content = down_sector_ks.content.decode('cp949')
    df = pd.read_csv(io.StringIO(decoded_content))
    return df

def refine_data(df):
    df.drop(df.columns[[2,3,5,6,11,12,13]], axis=1, inplace=True)
    df.columns = ['id', 'name', 'close', 'open', 'high', 'low', 'volume']
    df['date'] = datetime.today().strftime('%Y-%m-%d')
    
    result = df.to_json(orient="records")
    if validate_dataframe(df):
        result = "{}"
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
    

def validate_dataframe(df):
    return df['close'].isnull().values.any()

def lambda_handler(event, context):
    df = get_daily_data()
    data = refine_data(df)
    store_data(data)

if __name__ == '__main__':
    lambda_handler('event', 'context')