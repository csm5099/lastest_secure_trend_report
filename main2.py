import feedparser
from collections import Counter
from soynlp.tokenizer import LTokenizer

def request():
    url = "http://www.dailysecu.com/rss/S1N2.xml"
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
    
    # 형태소 분석기를 이용한 키워드 추출
    # 여기서는 LTokenizer 사용
    word_extractor = LTokenizer()
    
    keywords = []
    for summary in all_summaries:
        words = word_extractor.tokenize(summary)
        keywords.extend(words)
    
    # 키워드 빈도 분석
    keyword_freq = Counter(keywords)
    
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

request()
