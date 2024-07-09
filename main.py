from flask import Flask, render_template, request, send_file
from docx import Document
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        option1 = request.form.get('option1')
        option2 = request.form.get('option2')
        option3 = request.form.get('option3')

        doc = Document("test.docx")  # 사용할 docx파일 이름 기입
        if option1:
            
            pass

        for paragraph in doc.paragraphs:
            if 'option1' in paragraph.text:
                paragraph.text = paragraph.text.replace('option1', option1)
            elif 'option1' in paragraph.text:
                paragraph.text = paragraph.text.replace('option2', option2)
            elif 'option1' in paragraph.text:
                paragraph.text = paragraph.text.replace('option3', option3)

        doc_filename = f"{option1}_{option2}_report.docx"
        
        doc.save(doc_filename)

        

        return send_file(doc_filename, as_attachment=True)
    return render_template('index.html')

# 이 스크립트가 직접 실행될 때 Flask 애플리케이션을 실행합니다.
if __name__ == '__main__':
    app.run(debug=True)
