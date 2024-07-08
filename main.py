import os, time, re
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import schedule

#arg result_docx는 동향 정보가 담긴 docx명 
def mail_sender(result_docx):
    now = datetime.now()
    day = now.strftime("%Y-%m-%d")
    load_dotenv()
    SECRET_ID = os.getenv("SECRET_ID")
    SECRET_PASS = os.getenv("SECRET_PASS")

    smtp = smtplib.SMTP('smtp.naver.com', 587)
    smtp.ehlo()
    smtp.starttls()

    smtp.login(SECRET_ID,SECRET_PASS)
    
    send_email = "enter_your_email"
    recv_email = "enter_your_email"

    msg = MIMEMultipart()
    msg['Subject'] = f"[{day}] 일간 정보 보안 동향"  
    msg['From'] = send_email          
    msg['To'] = recv_email      

    text = f"안녕하세요\n {day} 일간 정보 보안 동향 워드 파일로 정리하여 보내드립니다."      
    contentPart = MIMEText(text) 
    msg.attach(contentPart)     

    file_name = result_docx
    with open(file_name, 'rb') as f : 
        etc_part = MIMEApplication( f.read() )
        etc_part.add_header('Content-Disposition','attachment', filename=f'[{day}]latest_secure_trend.docx')
        msg.attach(etc_part)

    email_string = msg.as_string()
    print(email_string)

    smtp.sendmail(send_email, recv_email, email_string)
    smtp.quit()

result_docx = '임해윤_certificate.docx'
def schedule_mail():
    schedule.every(1).minutes.do(mail_sender(result_docx))

schedule_mail()
