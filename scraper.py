from email import message
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import smtplib
from dotenv import load_dotenv 
import os
import json
from email.mime.text import MIMEText
from email.header import Header
import ssl
bdjobs_url="https://jobs.bdjobs.com/jobsearch.asp?fcatId=8&icatId="
load_dotenv()   
#GETTING DRIVER READY
options=Options()
options.binary_location='C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver=webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe',options=options)

def job_details(job):
    title=job.find_element(By.TAG_NAME,'a')
    url = title.get_attribute('href')
    company_name=job.find_element(By.CLASS_NAME,"comp-name-text")
    location_name=job.find_element(By.CLASS_NAME,"locon-text-d")
    experience= job.find_element(By.CLASS_NAME,'exp-text-d')
    deadline=job.find_element(By.CLASS_NAME,"dead-text-d")

    return {
        'title':title.text,
        'url':url,
        'company_name':company_name.text,
        'location_name':location_name.text,
        'experience':experience.text,
        'deadline':deadline.text
    }


def send_email(body):

    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()   

        SENDER_EMAIL = 'forthrowawaypurpose@gmail.com'
        RECEIVER_EMAIL = 'forthrowawaypurpose@gmail.com'
        SENDER_PASSWORD = os.environ.get('gmail_pass')
        
        subject = 'YouTube Trending Videos'

        email_text = f"""
        From: {SENDER_EMAIL}
        To: {RECEIVER_EMAIL}
        Subject: {subject}
        {body}
        """

        server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
        server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
        server_ssl.close()

    except:
        print('Something went wrong...')
if __name__=="__main__":
    
    #Fetching page
    driver.get(bdjobs_url)
    print("Page Title:", driver.title)

    #Found Jobs
    datas=driver.find_elements(By.XPATH,'//div[contains(@class,"jobs-wrapper")]')
    print(f'Fetching {len(datas)} Jobs')

    #Top 10 jobs that might interest you
    jobs_data = [job_details(job) for job in datas[:10]]

    #Saving in CSV   
    jobs_df=pd.DataFrame(jobs_data)
    print(jobs_df)
    jobs_df.to_csv('jobs.csv',index=None)
    
    print('Sending jobs data through email')
    body = json.dumps(jobs_data,indent=2)
    
    send_email(body)