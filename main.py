import feedparser


def request():
    url = "http://www.dailysecu.com/rss/S1N2.xml"
    feeds = feedparser.parse(url)
    print(feeds)


request()
