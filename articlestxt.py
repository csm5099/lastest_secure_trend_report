import time
from ftplib import FTP
from dotenv import load_dotenv
import os
import datetime


# Generate filename based on current date
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}_articles.txt"

    # Save articles to a text file with the generated filename
    with open(filename, 'w', encoding='utf-8') as file:
        for article in articles:
            file.write(article + '\n')

    # Upload file to FTP server
    ftp_host = os.getenv('FTP_HOST')
    ftp_user = os.getenv('FTP_USER')
    ftp_passwd = os.getenv('FTP_PASS')

    try:
        ftp = FTP(ftp_host)
        ftp.login(user=ftp_user, passwd=ftp_passwd)
        
        with open(filename, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
        
        print(f"File '{filename}' uploaded successfully to FTP server.")

    except Exception as e:
        print(f"FTP Error: {e}")
    finally:
        ftp.quit()

    return articles




FTP_HOST=your_ftp_host
FTP_USER=your_ftp_username
FTP_PASS=your_ftp_password
making .env
