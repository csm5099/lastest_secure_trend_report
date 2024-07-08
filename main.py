import feedparser
import requests


def request():
    url = "http://www.dailysecu.com/rss/S1N2.xml"
    feeds = feedparser.parse(url)
    print(feeds)
    print('피드 제목:', feeds.feed.title)
    print('피드 설명:', feeds.feed.description)
    print('아이템 개수:', len(feeds.entries))
    # item
    for entry in feeds.entries:
        print('제목:', entry.title)
        print('링크:', entry.link)
        print('요약:', entry.summary)
        print('게시일:', entry.published)   
request()