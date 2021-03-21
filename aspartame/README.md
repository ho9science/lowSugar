# aspartame
아스파탐은 특정 사이트의 데이터를 크롤링하고 특정 조건에 맞추어 정리한 후 구글 스프레드 시트로 데이터를 생성하고 특정 유저의 구글 계정을 공유하고 이를 메일로 보낼 수 있습니다.

## prerequisite
python 3.8 환경에서 테스트하고 실행을 확인하였습니다.

1. python 라이브러리
```
pip install selenium
pip install pandas
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

2. 크롬 드라이버
현재 운영체제에서 사용하고 있는 브라우저 드라이버를 설치합니다. 버전도 맞춰서 다운로드해주세요.
[크롬 드라이버 다운로드](https://sites.google.com/a/chromium.org/chromedriver/downloads)

3. 구글 시트 api
[구글 시트 api 가이드](https://developers.google.com/sheets/api/guides/concepts)
[구글 클라우드 플랫폼](https://console.cloud.google.com/)에서 google sheets api를 검색하고 사용하기 버튼을 누르세요.

4. 구글 드라이브 api
[구글 드라이브 api 가이드](https://developers.google.com/drive/api/v3/quickstart/python)
[구글 클라우드 플랫폼](https://console.cloud.google.com/)에서 google drive api를 검색하고 사용하기 버튼을 누르세요.

5. credential.json
구글 클라우드 플랫폼 - API 및 서비스 - 사용자 인증 정보에서 OAuth2.0 클라이언트 ID를 생성하고 credential.json을 다운로드 받으세요. credential.json의 형식은 다음과 같습니다.
```
{
    "web": {
        "client_id": "apps.googleusercontent.com",
        "project_id": "henry-bot",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "",
        "redirect_uris": []
    }
}
```

5. 구글 smtp
[Gmail](http://gmail.com/) 설정에서 전달 및 POP/IMAP탭에서 IMAP을 사용하세요.
[구글 계정 보안](https://myaccount.google.com/security)에서 앱비밀번호를 생성하세요.
```
  s.login(sender, '{앱비밀번호}')
```

## 로컬 사용법
```
python under_value.py
```

## 조건
현재 데이터 정제를 위한 특정 조건은 다음과 같습니다.
operating profit : x > 0
PBR(price book value ratio) : 0 < x <0.7
PER(price earning ratio) : 0 < x < 11.5
PSR(price selling ratio) : x < 0.55
