import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def get_articles():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36"
    }

    links = []

    for i in range(1, 11):
        outter_url = f"http://www.dailysecu.com/news/articleList.html?page={i}&total=13290&box_idxno=&sc_section_code=S1N2&view_type=sm"
        outter_req = requests.get(outter_url, headers=headers)
        outter_soup = BeautifulSoup(outter_req.text, "lxml")
        outter_tags = outter_soup.select(
            "#user-container > div > div > section > article > div > section > div > div > a"
        )
        for outter_tag in outter_tags:
            links.append(f"http://www.dailysecu.com{outter_tag.get('href')}")

    articles = []
    for link in links:
        inner_req = requests.get(link, headers=headers)
        inner_soup = BeautifulSoup(inner_req.text, "lxml")
        inner_tags = inner_soup.select("#user-container > div > div > section > div p")
        article = ""
        for p_tag in inner_tags:
            if p_tag.text.startswith("▷") or p_tag.text.startswith("★"):
                continue
            article += p_tag.text.strip()
        articles.append(article)

    return articles

def translate_articles(articles):
    translator = GoogleTranslator(source='auto', target='en')
    translated_articles = []
    for article in articles:
        try:
            translation = translator.translate(article)
            translated_articles.append(translation)
        except Exception as e:
            print(f"Error translating article: {e}")
            translated_articles.append(article)  # 실패한 경우 원본 텍스트 추가
    return translated_articles

def extract_keywords(translated_articles):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(translated_articles)
    terms = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.max(0).toarray()[0]
    word_tfidf_tuples = [(term, score) for term, score in zip(terms, tfidf_scores)]
    word_tfidf_tuples.sort(key=lambda x: x[1], reverse=True)

    # 상위 20개 키워드 출력
    print("{:<15} {}".format("Keyword", "TF-IDF Score"))
    print("=" * 30)
    for term, score in word_tfidf_tuples[:20]:
        print("{:<15} {:.2f}".format(term, score))

    return word_tfidf_tuples[:20]

def main():
    articles = get_articles()
    translated_articles = translate_articles(articles)
    top_keywords = extract_keywords(translated_articles)
    return top_keywords

if __name__ == "__main__":
    main()

