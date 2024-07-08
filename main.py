from bs4 import BeautifulSoup
import requests, time
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator
from docx import Document
from datetime import datetime


def cal_trend():

    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"
        }

    links=[]

    for i in range(1,2):
        outter_url = f"http://www.dailysecu.com/news/articleList.html?page={i}&total=13290&box_idxno=&sc_section_code=S1N2&view_type=sm"
        outter_req = requests.get(outter_url, headers=headers)
        outter_soup = BeautifulSoup(outter_req.text, "lxml")
        outter_tags = outter_soup.select(
            "#user-container > div > div > section > article > div > section > div > div > a"
        )#user-container > div > div > section > article > div > section > div > div.list-dated
        for outter_tag in outter_tags:
            links.append(f"http://www.dailysecu.com{outter_tag.get("href")}")
            #article-view-content-div > p
            #user-container > div > div > section > article > div > section > div > p > a
    articles=[]
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
        
        
    translator = Translator()
    i = 0
    for index, article in enumerate(articles):
        i+=1
        print(i)
        translated_article = translator.translate(f"{article}",src='ko', dest='en')
        print(translated_article)
        articles[index] = translated_article.text

    # TF-IDF 벡터화 객체 생성
    vectorizer = TfidfVectorizer()

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

    # 상위 20개 단어 출력
    print("{:<15} {}".format("단어", "TF-IDF 점수"))
    print("=" * 30)
    for term, score in word_tfidf_tuples[:20]:
        print("{:<15} {:.2f}".format(term, score))
    
    return word_tfidf_tuples[:20]

def dhodkseho(word_tfidf_tuples):
    try:
        # 워드 보고서 탬플릿 열기
        doc = Document("template.docx")

        # 날짜 데이터 가져오기
        now = datetime.now()
        day = now.strftime('%Y-%m-%d')
        with open('tt.txt', 'w', encoding='utf-8') as File:
        # 상위 20개 단어 출력
            print("{:<15} {}".format("단어", "TF-IDF 점수"))
            print("=" * 30)
            for term, score in word_tfidf_tuples[:20]:
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

            return True
    except Exception as e:
        print(f'실패 이유 {e}')
        return False


def main():
        # cal_trend() 에서 반환되는 값 저장
        top_words = cal_trend()
        # dhodkseho() 로 전달
        dhodkseho(top_words)

if __name__ == "__main__":
    main()