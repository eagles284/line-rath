import feedparser
import requests
from unicodedata import east_asian_width
import wikipedia
import re
from bs4 import BeautifulSoup
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt


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

# ====================================
# Google News
# ====================================
def google_news():
    # RSS Feed of yahoo news doesn't contain thumbnail image.
    url = 'https://news.google.com/news?hl=id&ned=us&ie=UTF-8&oe=UTF-8&topic=po&output=rss'
    parsed = feedparser.parse(url)
    return parsed.entries

# ================
# Grafik Persamaan
# ================
# def plot():
#     ############# Linear Equation of y = (3x - 4) / 2

#     # Create a dataframe with an x column containing values from -10 to 10
#     # df = pd.DataFrame({'x': range(-10, 11)})

#     # Define slope and y-intercept
#     # m = 1.5
#     # yInt = -2

#     # Add a y column by applying the slope-intercept equation to x
#     # df['y'] = m*df['x'] + yInt
#     # print(df)

#     # Plot the line

#     x = [0, 1]
#     y = [1, 0]

#     plt.plot(x, y, color="red")
#     # plt.xlabel('x')
#     # plt.ylabel('y')
#     plt.axhline()
#     plt.axvline()
#     # plt.grid()

#     # label the y and x - intercept

#     # plot the slope from the y-intercept for 1x
#     # mx = [0, 1]
#     # my = [yInt, yInt + m]
#     # plt.plot(mx,my, color='red', lw=5)
#     plt.savefig('math.png')
    
    # plt.show()

# ==================
# Screenshot Website
# ==================
