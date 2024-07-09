from bs4 import BeautifulSoup
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from googletrans import Translator


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


# 키워드 리포트 생성
def create_keyword_report():
    links = collect_links()
    articles = extract_descriptions(links)
    translated = translate_for_tfidf(articles)
    tfidf = cal_tfidf(translated)
    print_tfidf(tfidf)


# 보안 뉴스 이슈 뉴스 제목과 링크 표 생성
def create_secure_issue_table():
    articles = []
    url = "https://www.dailysecu.com/news/articleList.html?sc_section_code=S1N2&view_type=sm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    tags = soup.select(
        "#user-container > div > div > section > article > div > section > div > div > a"
    )
    for tag in tags:
        title=""
        link=""
        if tag.find("strong"):
            title = f"{tag.find("strong").text}"
            link = f"http://www.dailysecu.com{tag.get('href')}"
            articles += [(title, link)]

    return articles


# 보안 뉴스 카테고리 별 보안  표 생성
def create_category_news():
    pass


def main():
    create_keyword_report()


if __name__ == "__main__":
    create_category_news()
