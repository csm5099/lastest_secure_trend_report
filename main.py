import feedparser


def parser_rss():
    url = "http://www.dailysecu.com/rss/S1N2.xml"
    feeds = feedparser.parse(url)

    if feeds.entries:
        for entry in feeds.entries:
            print(entry.title)
            print(entry.description)
            print(entry.author)
            print(entry.published)
            print(entry.link)
    else:
        print("none")


parser_rss()
