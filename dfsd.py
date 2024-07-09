import ftplib

hostname = "192.168.217.128"

ftp = ftplib.FTP(hostname)

ftp.login('msfadmin','msfadmin')

ftp.retrlines('LIST')
ftp.storbinary('STOR newfile.txt', open('newfile.txt', 'rb'))

ftp.quit()