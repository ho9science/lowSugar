import feedparser
import os
import json
import requests

def send_message(text, link):
    header = {"Authorization": 'Bearer {token}', "Content-Type":"application/x-www-form-urlencoded"}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" 

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": link
        },
        "button_title": "공시 확인"
    }
    data = {"template_object": json.dumps(post)}
    response = requests.post(url, headers=header, data=data)
    if not response:
        print('An error has occurred: ')
    return response.status_code

def get_feed(matches):
    NewsFeed = feedparser.parse("http://dart.fss.or.kr/api/todayRSS.xml")

    print ('Number of RSS posts :', len(NewsFeed.entries))
    
    for entry in NewsFeed.entries:
        if any(x in entry.title for x in matches):
            send_message(entry.title, entry.link)

def lambda_handler(event, context):
    with open('favorite.json') as f:
        data = json.load(f)
    get_feed(data['key'])
    return { 
        'message' : 'success'
    }

if __name__ == '__main__':
    with open('favorite.json') as f:
        data = json.load(f)
    get_feed(data['key'])
