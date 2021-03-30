# saccaharin
사카린은 csv데이터를 다운로드 받아 특정 조건에 맞추어 정리한 후 AWS dynamodb로 보낼 수 있습니다.

## prerequisite
python 3.8 환경에서 테스트하고 실행을 확인하였습니다.

1. python 라이브러리
```
pip install selenium
pip install pandas
pip install awscli
pip install boto3
```

2. AWS dynamodb
[다이나모DB 시작하기](https://aws.amazon.com/ko/dynamodb/getting-started/)
```
aws에서 dynamodb table을 만들어주세요.
예시 json입니다.
partition key와 sort key는 꼭 필요합니다.
{
    'id': '202103',
    'name': 'henry',
    'close': 2000,
    'open': 2000,
    'high': 2600,
    'low': 1400,
    'volume': 200000,
    'date': '2021-03-31'
}
```

3. awscli
awscli를 사용하기 위해서는 [AWS](https://aws.amazon.com/)에서 내 보안 자격 증명 - 엑세스 키를 생성하세요.
```
$ aws configure
$ AWS Access Key ID :
$ AWS Secret Acess Key :
$ Default region name :
$ Default output format :
```

3. boto3
boto3는 Python용 AWS SDK입니다. 
[boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 로컬 사용법
```
python refine_value.py
```
