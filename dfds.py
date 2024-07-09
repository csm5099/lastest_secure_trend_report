import feedparser
from collections import Counter
from soynlp.tokenizer import LTokenizer
from googletrans import Translator
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def translate_and_extract_keywords(url):
    feeds = feedparser.parse(url)
    print('피드 제목:', feeds.feed.title)
    print('피드 설명:', feeds.feed.description)
    print('아이템 개수:', len(feeds.entries))
    
    all_summaries = []
    articles = []
    
    # 아이템 수집
    for entry in feeds.entries:
        summary = entry.summary
        all_summaries.append(summary)
        articles.append({
            'title': entry.title,
            'link': entry.link,
            'summary': summary,
            'published': entry.published
        })
    
    # 영어로 기사 번역 및 키워드 추출
    translator = Translator()
    word_extractor = LTokenizer()
    lemmatizer = WordNetLemmatizer()
    english_articles = []
    english_keywords = []
    
    for summary in all_summaries:
        # 기사를 영어로 번역
        translated = translator.translate(summary, src='auto', dest='en')
        english_summary = translated.text
        english_articles.append(english_summary)
        
        # 영어 기사에서 명사 추출
        words = word_extractor.tokenize(english_summary)
        
        # NLTK를 사용하여 명사 추출
        nouns = [word.lower() for (word, pos) in pos_tag(word_tokenize(english_summary)) if pos.startswith('NN') and word.isalnum()]
        
        # 불용어 제거
        stop_words = set(stopwords.words('english'))
        nouns = [lemmatizer.lemmatize(word) for word in nouns if word not in stop_words]
        
        english_keywords.extend(nouns)
    
    # 키워드 빈도 분석
    keyword_freq = Counter(english_keywords)
    
    # 빈도수가 높은 키워드 10개 추출
    most_common_keywords = keyword_freq.most_common(10)
    
    print("\n빈도수가 높은 키워드:")
    for word, freq in most_common_keywords:
        print(f"{word}: {freq}")
    
    # 키워드가 포함된 기사 출력
    print("\n키워드가 포함된 기사들:")
    for keyword, _ in most_common_keywords:
        print(f"\n키워드: {keyword}")
        for article in articles:
            if keyword in article['summary']:
                print(f"제목: {article['title']}")
                print(f"링크: {article['link']}")
                print(f"요약: {article['summary']}")
                print(f"게시일: {article['published']}")
                print('-' * 80)

# 실행 예시
url = "http://www.dailysecu.com/rss/S1N2.xml"
translate_and_extract_keywords(url)
