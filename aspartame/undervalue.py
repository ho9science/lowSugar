import selenium
from selenium import webdriver

import pandas as pd 

import smtplib

from email.mime.text import MIMEText
from datetime import datetime


target_url = [""]

driver = webdriver.Chrome('./driver/chromedriver')
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

recipients = []
sender = ""
today = datetime.today().strftime('%Y-%m-%d')

subject = "코스피: 저평가 가치주 "+today
msg = MIMEText(df.to_string())
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = ", ".join(recipients)

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(sender, '')
s.sendmail(sender, recipients, msg.as_string())
s.quit()
