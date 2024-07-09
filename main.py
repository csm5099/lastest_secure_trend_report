from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator
from docx import Document
from datetime import datetime
import ftplib


# 뉴스 페이지를 순회하며 뉴스의 링크를 수집
def collect_links():
    links = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"
    }
    for i in range(1, 11):
        outter_url = f"http://www.dailysecu.com/news/articleList.html?page={i}&total=13290&box_idxno=&sc_section_code=S1N2&view_type=sm"
        outter_req = requests.get(outter_url, headers=headers)
        outter_soup = BeautifulSoup(outter_req.text, "lxml")
        outter_tags = outter_soup.select(
            "#user-container > div > div > section > article > div > section > div > div > a"
        )
        links += [f"http://www.dailysecu.com{tag.get('href')}" for tag in outter_tags]
    return links


# 뉴스의 본문을 수집
def extract_descriptions(links):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"
    }
    i = 0
    articles = []
    for link in links:
        inner_req = requests.get(link, headers=headers)
        inner_soup = BeautifulSoup(inner_req.text, "lxml")
        inner_tags = inner_soup.select("#user-container > div > div > section > div p")
        p = ""
        for p_tag in inner_tags:
            if p_tag.text.startswith("▷") or p_tag.text.startswith("★"):
                continue
            p += p_tag.text.strip()
        articles.append(str(p))
        i +=1
        if i == 40:
            break

    return articles


# tf-idf를 위해 내용을 영어로 번역함
def translate_for_tfidf(articles):
    translator = Translator(
        service_urls=[
            "translate.google.com",
            "translate.google.co.kr",
        ]
    )

    i = 0
    for index, article in enumerate(articles):
        print(i)
        i += 1
        try:
            # 언어 감지
            detected = translator.detect(article)
            if detected is not None:
                # 텍스트 번역
                translated = translator.translate(article, src=detected.lang, dest="en")
                if translated is not None:
                    articles[index] = translated.text
                else:
                    print("Translation failed: No response from API.")
            else:
                print("Language detection failed: No response from API.")

        except Exception as e:
            print(f"An error occurred: {e}")

    return articles


# 단어의 중요도를 평가하기위한 tf-idf
def cal_tfidf(articles):
    # TF-IDF 벡터화 객체 생성
    vectorizer = TfidfVectorizer(stop_words="english")

    # TF-IDF 행렬 계산
    tfidf_matrix = vectorizer.fit_transform(articles)

    # 단어 목록
    terms = vectorizer.get_feature_names_out()

    # 각 단어의 TF-IDF 점수 계산
    tfidf_scores = tfidf_matrix.max(0).toarray()[0]

    # 단어와 TF-IDF 점수를 튜플 리스트로 저장
    word_tfidf_tuples = [(term, score) for term, score in zip(terms, tfidf_scores)]

    # TF-IDF 점수 기준으로 내림차순 정렬
    word_tfidf_tuples.sort(key=lambda x: x[1], reverse=True)

    return word_tfidf_tuples


# 상위 단어 40개 출력
def print_tfidf(word_tfidf_tuples):
    print("{:<15} {}".format("단어", "TF-IDF 점수"))
    print("=" * 30)
    for term, score in word_tfidf_tuples[:40]:
        print("{:<15} {:.2f}".format(term, score))

def dhodkseho(word_tfidf_tuples):
    try:
        print(word_tfidf_tuples)
        # 워드 보고서 탬플릿 열기
        doc = Document("template.docx")

        # 날짜 데이터 가져오기
        now = datetime.now()
        day = now.strftime('%Y-%m-%d')
        with open('tt.txt', 'w', encoding='utf-8') as File:
        # 상위 20개 단어 출력
            print("{:<15} {}".format("단어", "TF-IDF 점수"))
            print("=" * 30)
            for term, score in word_tfidf_tuples[:40]:
                print("{:<15} {:.2f}".format(term, score))
                File.write('{:<15}\t{:.2f}\n'.format(term, score))
        with open('tt.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
            i = 0

            # 돌면서 단어 추가
            for line in lines:
                paragraphs = doc.paragraphs
                for paragraph in doc.paragraphs:
                    if 'DATE' in paragraph.text:
                        paragraph.text = paragraph.text.replace('DATE', day)
                
                # course 변수를 올바른 단락으로 설정
                course = paragraphs[6]
                
                # course.text가 정확히 'COURSE'인지 확인
                if 'COURSE' in course.text:
                    new = course.add_run(f'\n{line.strip()}\n')
                    i += 1

            if i >= len(lines):
                course.text = course.text.replace('COURSE', '')
                course.add_run('\n' + '=' * 30 + '\n')

            doc.save('123.docx')
        hostname = "192.168.217.128"
        ftp = ftplib.FTP(hostname)

        ftp.login('msfadmin', 'msfadmin')
        
        with open('123.docx', 'rb') as file:
            ftp.storbinary('STOR 123.docx', file)

        ftp.quit()

        return True
    except Exception as e:
        print(f'실패 이유 {e}')
        return False

def create_secure_trend():
    links = collect_links()
    articles = extract_descriptions(links)
    translated = translate_for_tfidf(articles)
    tfidf = cal_tfidf(translated)
    print_tfidf(tfidf)
    dhodkseho(tfidf)


def main():
    create_secure_trend()


if __name__ == "__main__":
    main()