import feedparser
import requests
from unicodedata import east_asian_width
import wikipedia

# ====================================
# Wikipedia Search
# ====================================
def wikipedia_search(word):
    """Search a word meaning on wikipedia."""
    wikipedia.set_lang('id')
    results = wikipedia.search(word)

    # get first result
    if results:
        page = wikipedia.page(results[0])
        msg = page.title + "\n" + page.url
    else:
        msg = '`{}` Tidak bisa menemukan kata yang dicari'.format(word)
    return msg

print(wikipedia_search("kucing"))

# ====================================
# Google News
# ====================================
def google_news():
    # RSS Feed of yahoo news doesn't contain thumbnail image.
    url = 'https://news.google.com/news?hl=id&ned=us&ie=UTF-8&oe=UTF-8&topic=po&output=rss'
    parsed = feedparser.parse(url)
    return parsed.entries
