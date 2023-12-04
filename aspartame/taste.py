from __future__ import print_function

from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd 

import smtplib

from email.mime.text import MIMEText
from datetime import datetime

import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def create_undervalue():
    target_url = ['https://finance.naver.com/sise/sise_rise.naver', 'https://finance.naver.com/sise/sise_steady.naver', 'https://finance.naver.com/sise/sise_fall.naver']
    driver = webdriver.Chrome()
    candidate = []
    driver.implicitly_wait(time_to_wait=5)

    for url in target_url:
        driver.get(url=url)
        driver.find_element(By.ID, 'option1').click()
        driver.find_element(By.ID, 'option2').click()
        driver.find_element(By.ID, 'option8').click()
        driver.find_element(By.ID, 'option14').click()
        driver.find_element(By.ID, 'option20').click()
        driver.find_element(By.ID, 'option6').click()
        driver.find_element(By.ID, 'option12').click()
        
        driver.find_element(By.ID, 'option4').click()
        driver.find_element(By.ID, 'option5').click()
        driver.find_element(By.ID, 'option17').click()
        driver.find_element(By.ID, 'option27').click()
        
        driver.find_element(By.ID, 'option10').click()
        driver.find_element(By.ID, 'option16').click()
        driver.find_element(By.ID, 'option22').click()

        driver.execute_script("fieldSubmit()")
        
        table_class = driver.find_element(By.CLASS_NAME, 'type_2')
        tbody = table_class.find_element(By.TAG_NAME, "tbody")
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            a = []
            if len(cols) < 2:
                continue
            else:
                if cols[5].text=="N/A" or cols[6].text=="N/A" or cols[7].text=="N/A" or cols[8].text=="N/A": #no info
                    continue
                a.append(cols[1].text) #name
                a.append(cols[2].text.replace(",", "")) #price
                a.append(cols[5].text.replace(",", ""))
                a.append(cols[6].text.replace(",", ""))
                a.append(cols[7].text.replace(",", ""))
                a.append(cols[8].text.replace(",", ""))
                a.append(cols[9].text.replace(",", ""))
                a.append(cols[10].text.replace(",", ""))
                a.append(cols[11].text.replace(",", ""))

            candidate.append(a)
    driver.close()
    df = pd.DataFrame(candidate)
    df = df.rename({0: 'name', 1: 'price', 2: '시가총액', 3: '매출액', 4:'자산총계', 5:'부채총계', 6:'영업이익', 7:'당기순이익', 8:'유보율'}, axis='columns')
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
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
              'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        print('exist token')
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            print('write token')
            token.write(creds.to_json())
    return creds

def createSheetAndUpdate(values):
    spreadsheet_id = ''
    range_name = 'A1:N2000'
    value_input_option = 'USER_ENTERED'
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = createCredential()

    service = build('sheets', 'v4', credentials=creds)
    today = datetime.today().strftime('%Y-%m-%d')

    title = today
    spreadsheet = {"properties": {"title": title}}
    spreadsheet = (
        service.spreadsheets()
        .create(body=spreadsheet, fields="spreadsheetId")
        .execute()
    )
    print(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
    spreadsheet_id = spreadsheet.get("spreadsheetId")
    update_values(spreadsheet_id, range_name, value_input_option, values)
    #shareSheet(spreadsheet_id)
    return spreadsheet.get('spreadsheetUrl')

def update_values(spreadsheet_id, range_name, value_input_option, _values):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds = createCredential()
    try:
        service = build("sheets", "v4", credentials=creds)
        body = {"values": _values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
  
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
    #send_mail(share_url)