from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator



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

print(cal_trend())
