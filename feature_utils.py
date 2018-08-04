import feedparser
import requests
from unicodedata import east_asian_width
import wikipedia

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