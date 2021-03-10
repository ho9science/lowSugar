from __future__ import print_function

import selenium
from selenium import webdriver

import pandas as pd 

import smtplib

from email.mime.text import MIMEText
from datetime import datetime

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def create_undervalue():
    target_url = []
      path = "./driver/chromedriver"
    driver = webdriver.Chrome(path)
    candidate = []
    driver.implicitly_wait(time_to_wait=5)

    for url in target_url:
        driver.get(url=url)
        option1 = driver.find_element_by_id("option1")
        option1 = driver.find_element_by_id("option2").click()
        option1 = driver.find_element_by_id("option8").click()
        option1 = driver.find_element_by_id("option14").click()
        option1 = driver.find_element_by_id("option20").click()

        option4 = driver.find_element_by_id("option4").click()
        option5 = driver.find_element_by_id("option5").click()
        option6 = driver.find_element_by_id("option6")
        option1 = driver.find_element_by_id("option12").click()
        option22 = driver.find_element_by_id("option22").click()
        option24 = driver.find_element_by_id("option24").click()

        driver.execute_script("fieldSubmit()")

        table_class = driver.find_element_by_class_name('type_2')
        rows = table_class.find_elements_by_tag_name("tr")
        
        for row in rows:
            cols = row.find_elements_by_tag_name("td")
            a = []
            if len(cols) < 2:
                continue
            else:
                if cols[7].text=="N/A" or cols[8].text=="N/A" or cols[9].text=="N/A" or cols[10].text=="N/A": #no info
                    continue
                a.append(cols[1].text) #name
                a.append(cols[2].text.replace(",", "")) #price
                a.append(int(cols[5].text.replace(",", "")))
                a.append(int(cols[6].text.replace(",", "")))
                a.append(int(cols[7].text.replace(",", "")))
                a.append(int(cols[8].text.replace(",", "")))
                per = float(cols[9].text.replace(",", ""))
                pbr = float(cols[10].text.replace(",", ""))
                psr = int(cols[6].text.replace(",", ""))/int(cols[7].text.replace(",", ""))
                weighted_average = per*0.4 + psr*0.4 + per*0.2
                a.append(per)
                a.append(pbr)
                a.append(psr)
                a.append(weighted_average)
                candidate.append(a)
    driver.close()
    df = pd.DataFrame(candidate)
    df = df[df[5] > 0] # no negative value
    df = df[df[7].between(0, 0.7)]
    df = df[df[6].between(0, 11.5)]
    df = df[df[8] < 0.55]
    df = df.rename({0: 'name', 1: 'price', 2: '거래량', 3: '시가총액', 4:'매출액', 5:'영업이익', 6:'per', 7:'pbr', 8:'psr', 9:'weighted_average'}, axis='columns')
    df = df.sort_values(by=['weighted_average'])
    return df

def send_mail(share_url):
    recipients = []
    sender = ""
    today = datetime.today().strftime('%Y-%m-%d')

    subject = today
    msg = MIMEText(share_url)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender, '')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

def createCredential():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def createSheetAndUpdate(values):
    spreadsheet_id = ''
    range_name = 'A1:N100'
    value_input_option = 'USER_ENTERED'
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = createCredential()

    service = build('sheets', 'v4', credentials=creds)
    today = datetime.today().strftime('%Y-%m-%d')

    title = today
    body = {
        'properties': {
            'title': title
        },
    }
    request = service.spreadsheets().create(body=body)
    response = request.execute()

    spreadsheet_id = response.get('spreadsheetId')
    
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption=value_input_option, body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))
    shareSheet(spreadsheet_id)
    return response.get('spreadsheetUrl')

def shareSheet(file_id):
    creds = createCredential()
    drive_service = build('drive', 'v3', credentials=creds)

    batch = drive_service.new_batch_http_request(callback=callback)
    user_permission = {
        'emailAddress': '',
        'type': 'user',
        'role': 'writer'
    }
    batch.add(drive_service.permissions().create(
            fileId=file_id,
            body=user_permission,
            fields='id',
    ))
    batch.execute()
    
def callback(request_id, response, exception):
    if exception:
        # Handle error
        print ("exception: %s" % exception)
    else:
        print ("Permission Id: %s" % response.get('id'))

if __name__ == '__main__':
    df = create_undervalue()
    sheet_list = [df.columns.values.tolist()] + df.values.tolist()
    share_url = createSheetAndUpdate(sheet_list)
    send_mail(share_url)