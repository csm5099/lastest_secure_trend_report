from flask import Flask, render_template, request
import ftplib

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/ftp_files', methods=['POST'])
def ftp_files():
    ftp_host = request.form['ftp_host']
    ftp_user = request.form['ftp_user']
    ftp_pass = request.form['ftp_pass']
    
    try:
        ftp = ftplib.FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)
        files = ftp.nlst()
        ftp.quit()
        return render_template('index_ftp.html', files=files)
    except ftplib.all_errors as e:
        return f"FTP 오류: {e}"

if __name__ == '__main__':
    app.run(debug=True)
