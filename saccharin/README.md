# saccaharin
사카린은 csv데이터를 다운로드 받아 특정 조건에 맞추어 정리한 후 AWS dynamodb로 보낼 수 있습니다.

selenium과 requests 라이브러리를 사용하는 두가지 케이스가 있습니다.


## prerequisite
python 3.8 환경에서 테스트하고 실행을 확인하였습니다.

1. python 라이브러리
```
pip install selenium or pip install requests
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

4. boto3
boto3는 Python용 AWS SDK입니다. 
[boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)


5. AWS lambda
request_refine_value는 AWS lambda에 배포하여 사용할 수 있습니다.

pandas는 numpy기반의 라이브러리이기 때문에 운영체제가 중요하여 단순 업로드 방식으로 lambda를 배포하지 못하기 때문에 다음과 같은 절차를 진행합니다.

[도커로 람다 계층 생성하기](https://aws.amazon.com/ko/premiumsupport/knowledge-center/lambda-layer-simulated-docker/)

- mkrdir docker, 하위 디렉토리 생성. 
```
├── requirements.txt
└── python/
    └── lib/
        └── python3.8/
            └── site-packages
```

- cd docker

- vi requirements.txt
```
requests>=2.25.1
pandas>=1.2.4
boto3>=1.17.51
```

- 도커 컨테이너 생성 : 도커 컨테이너를 생성하고 pip로 설치합니다. aws의 public ecr을 사용하면 비용청구가 되지 않습니다.
```
docker run -v "$PWD":/var/task "public.ecr.aws/sam/build-python3.8" /bin/sh -c "pip install -r requirements.txt -t python/lib/python3.8/site-packages/; exit"
```

- 파이썬 폴더 압축 : 
```
zip -r requests_refine.zip python > /dev/null
```

- 계층 생성 : 
```
aws lambda publish-layer-version --layer-name {layer_name} --description "{description}" --zip-file fileb://requests_refine.zip --compatible-runtimes "python3.8"
```

- 계층 사용 : 
```
aws lambda update-function-configuration --layers arn:aws:lambda:{location}:{id}:layer:{layer_name}:1 --function-name {lambda_function_name}
```

- aws의 dynamodb를 사용하기 위해서는 IAM으로 권한을 설정해야합니다. 다음의 권한을 가진 IAM을 생성하고 lambda 함수에 권한을 부여해주세요.
[dynamodb 접근을 위한 IAM 권한 생성하기](https://aws.amazon.com/ko/blogs/security/how-to-create-an-aws-iam-policy-to-grant-aws-lambda-access-to-an-amazon-dynamodb-table/)

+ DescribeTable
+ DescribeTableReplicaAutoScaling
+ DescribeTimeToLive
+ BatchWriteItem
+ CreateTable
+ PutItem
+ UpdateItem
+ UpdateTable
+ UpdateTableReplicaAutoScaling
+ UpdateTimeToLive

6. cloudwatch
aws cloudwatch로 이벤트 패턴 또는 일정을 설정하여 대상을 호출할 수 있습니다.

- [클라우드워치 이벤트](https://docs.aws.amazon.com/ko_kr/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html)
- [클라우드워치 cron 표현식](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html)
```
Cron표현식(UTC기준)
0 12 ? * MON-FRI *
```

## 로컬 사용법
```
python selenium_refine_value.py

python requests_refine_value.py
```

