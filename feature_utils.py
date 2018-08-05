import feedparser
import requests
from unicodedata import east_asian_width
import wikipedia
import re
from bs4 import BeautifulSoup
import datetime
import contextlib
import selenium.webdriver as webdriver
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

currentDate = ""
realCurrentDate = ""

# ==================
# Screenshot Website
# ==================
def ssweb(url):
    global currentDate, realCurrentDate
    currentDate = str(datetime.datetime.now().time())
    datenow = currentDate.replace(":","")
    realCurrentDate = datenow

    rawinputstring = url.replace(" ", "")
    inputstring = rawinputstring.replace("/webss", "")
    print(inputstring)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    driver = webdriver.Chrome(chrome_options=options)
    
    driver.get('https://python.org')
    driver.save_screenshot("/static/screenshot.png")
    
    driver.close()

ssweb("/webss www.google.com")

# ================
# Grafik Persamaan
# ================
def plot(persamaan):

    global currentDate, realCurrentDate
    currentDate = str(datetime.datetime.now().time())
    datenow = currentDate.replace(":","")
    realCurrentDate = datenow

    rawinputstring = persamaan.replace(" ", "")
    inputstring = rawinputstring.replace("/grafik", "")
    print(inputstring)

    if "x" in inputstring and "y" in inputstring and "=" in inputstring and "/" not in inputstring and "*" not in inputstring:
        
        try:
            plt.clf()
            removex = inputstring.replace(" ", "").split("x")
            removey = removex[1].split("y")
            removee = removey[1].split("=")

            xraw = int(removex[0])
            yraw = int(removey[0])
            e = int(removee[1])

            x = e/xraw
            y = e/yraw
            print("x:",xraw,"y:",yraw,"e:",e)
            print("x:",x,"y:",y,"e:",e)

            # Create a dataframe with an x column containing values from -10 to 10
            # df = pd.DataFrame({'x': range(-10, 11)})

            # Define slope and y-intercept
            # m = 1.5
            # yInt = -2

            # Add a y column by applying the slope-intercept equation to x
            # df['y'] = m*df['x'] + yInt
            # print(df)

            # Plot the line
            print("Going to plot")
            xi = [0, x]
            yi = [y, 0]

            plt.plot(xi, yi, color="red")
            # plt.xlabel('x')
            # plt.ylabel('y')
            plt.axhline()
            plt.axvline()    
            plt.grid()
            print("Going to plot...2")
            strx = str(x)
            stry = str(y)

            # label the y and x - intercept
            plt.axvspan(x, y, facecolor='g', alpha=0)
            plt.annotate(strx[0:5],(x,0), color='green')
            plt.annotate(stry[0:5],(0,y), color='green')
            print("PLOT SUCCESS")
            # plot the slope from the y-intercept for 1x
            # mx = [0, 1]
            # my = [yInt, yInt + m]
            # plt.plot(mx,my, color='red', lw=5)
            print("Creating file....")

            plt.savefig('static/' + realCurrentDate + ".png")

            print("Create file success")
            print("Generating URL")

            fileurl = "https://trombosit.herokuapp.com/static/" + realCurrentDate + ".png"

            print("fileurl:", fileurl)

            return str(fileurl)

            # plt.show()  # REMOVE THIS ON EXECUTE!!!
            
        except IndexError:
            return IndexError
    else:
            print("Format error")
            return

# plot("3x+2y=6")
# plot("5x+4y=20")
