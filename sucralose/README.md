# sucralose
수크랄로스는 특정 소스로부터 xml을 파싱하여 저장할 수 있습니다.

## prerequisite
python 3.8 환경에서 테스트하고 실행을 확인하였습니다.

1. python 라이브러리
```
다음 라이브러리를 추가 설치해야 합니다.

pip install pandas
pip install requests
pip install awscli
pip install boto3
```

2. aws dynamoDB
aws에서는 dynamoDB를 프리티어로 제공하고 있습니다. 프리티어는 기본으로 25GB의 데이터 스토리지를 제공합니다. 
약 800만건을 저장하더라도 600MB정도의 용량을 차지하기 때문에 유용하게 사용할 수 있습니다.

프로비저닝 용량 모드로 사용할 수 있습니다. 기본 설정은 초당 5개로 약6000개의 데이터를 10분의 쓰기 시간이 소요되지만 초당 100개로 설정할 경우 약 1분으로 쓰기 시간을 줄일 수 있습니다. 40000개 이상은 사전승인을 받아야 합니다.

- 프로비저닝 용량 늘리는 방법
```
DynamoDB - 테이블 - 용량 - 오토스케일링 쓰기용량 체크
```

- 테이블 항목 예시
```
partition key와 sort key는 꼭 필요합니다.
{
    'id': '000001',
    'close': 2000,
    'open': 2000,
    'high': 2600,
    'low': 1400,
    'volume': 200000,
    'date': '2021-04-10'
}
```

3. stockcode.json
현재 stockcode.json에 저장된 리스트를 바탕으로 소스에 접근하고 있습니다.

- stockcode.json예시
```
{
    "005930": {
        "name": "삼성전자"
    },
    "091990": {
        "name": "셀트리온헬스케어"
    }
}
```

## 로컬 사용법
```
python store_data.py
```