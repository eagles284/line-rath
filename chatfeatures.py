from random import randint
from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
    LocationSendMessage, LocationMessage, PostbackAction, URIAction, MessageAction,
    ImageSendMessage,
)
from utility import line_bot_api
import feature_chatai
import feature_utils
from bs4 import BeautifulSoup
import re
import requests
import datetime
import time
import contextlib


aimode = False
helptext = """===== TROMBOSIT V1.52 =========
||  /help /trombosit
||  /pembuat
||  /jadwal *Mapel XI IPS 2
||  /chatmode (on/off)
||  /love (orang1, orang2)
||  /wikipedia (search...)
||  /grafik (ax + by = c)
||  /screenshot (web url)
||  /instagram (username)
||
||  *Tip: masukkan perintah diawali
||   garis miring (/) dan huruf kecil
=============================="""


def textreply(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

def imgreply(event, imgurl):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url=imgurl,
            preview_image_url=imgurl
        ))
# def _news_carousel(entry):
#     summary_soup = BeautifulSoup(entry.summary, "html.parser")
#     # summary has img tag which has no src attribute like:
#     # <img alt="" height="1" width="1"/>
#     images = [x for x in summary_soup.find_all('img') if x.has_attr('src')]
#     if len(images) == 0:
#         return
#     thumbnail_url = images[0]['src']

#     # carousel column text is accepted until 60 characters when set the thumbnail image.
#     carousel_text = summary_soup.find_all('font')[5].contents[0]
#     carousel_text = carousel_text[:57] + '...' if len(carousel_text) > 60 else carousel_text

#     # carousel column title is accepted until 40 characters.
#     title = entry.title[:37] + '...' if len(entry.title) > 40 else entry.title

#     return CarouselColumn(
#         thumbnail_image_url=thumbnail_url,
#         title=title,
#         text=carousel_text,
#         actions=[URITemplateAction(label='Buka di Browser', uri=entry.link)],
#     )



# def customresponse(event, received, send):
#     msg = event.message.text
#     if msg == received:
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=send))
#     return

# /help /trombosit
def help(event):
    msg = event.message.text
    if msg == "/help":
        textreply(event, helptext)
    elif msg == "/trombosit":
        textreply(event, helptext)
    return


# /pembuat
def creator(event):
    msg = event.message.text
    if msg == "/pembuat":
        textreply(event, "Seseorang yang sangat membenci Bahasa Mandarin :)")
    elif msg == "/jadwal":
        imgreply(event, 'https://trombosit.herokuapp.com/static/jadwal.jpg')
    return

# /chatmode on/off     
def aimodeon(event):
    global aimode
    msg = event.message.text
    if msg == "/chatmode on":
        
        aimode = True
        textreply(event, "Chatting mode on")
    elif msg == "/chatmode off":
        
        aimode = False
        textreply(event, "Chatting mode off")

def reply(msgserv):
    return msgserv

def aireply(event):
    msg = event.message.text
    global aimode
    if aimode:
        airesponse = feature_chatai.chat(msg)
        textreply(event, str(airesponse))
    
# /love
def love(event):
    msg = str(event.message.text)
    if msg.startswith("/love"):
        
        proceedmsg = msg.replace("/love", "").split(",")
        int_love = randint(0,100)
        replystring = "Hasil percintaan: \n" + proceedmsg[0] + " &" + proceedmsg[1] + " adalah " + str(int_love) + "%"
        textreply(event, replystring)
        # print(replystring)

# /wikipedia
def wiki(event):
    msg = str(event.message.text)
    if msg.startswith("/wikipedia"):

        cleanmsg = msg.replace("/wikipedia","")
        replystring = str(feature_utils.wikipedia_search(cleanmsg))
        textreply(event, replystring)

# /screenshot
# /instagram
def webss(event):
    msg = str(event.message.text)

    if msg.startswith("/screenshot") or msg.startswith("/instagram"):
        wFile = feature_utils.ssweb(msg)
        if wFile is not None:
         
            print("IMG File is:", wFile)

            time.sleep(2)
            
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url=wFile,
                    preview_image_url=wFile
                ))
            
        else:
            textreply(event, "Screenshot gagal, cobalah untuk screenshot ulang.")

# /grafik
bukanUjian = True
def grafik(event):
    global bukanUjian
    msg = str(event.message.text)
    if msg == "/ujian true":
        bukanUjian = False
        textreply(event, "Lagi ujian : ON")
    elif msg == "/ujian false":
        bukanUjian = True
        textreply(event, "Lagi ujian : OFF")
    if bukanUjian:
        if msg.startswith("/grafik"):
            msg.replace("/grafik", "")

            print("Command is", msg)
            fileurl = feature_utils.plot(msg)
            time.sleep(2)
            print("File url is", fileurl)

            if fileurl is not None:
                line_bot_api.reply_message(
                    event.reply_token,
                    ImageSendMessage(
                        original_content_url=fileurl,
                        preview_image_url=fileurl
                    ))
            else:
                textreply(event, "Tolong masukkan dengan format: \n /grafik ax + by = c \n Contoh: \n /grafik 1x + 2y = 6")
    else:
        if msg.startswith("/grafik"):
            textreply(event, "Lagi ujian cuk, anda tercyduk!!")

# /berita
# def berita(event):
#     msg = str(event.message.text)
#     if msg == "/berita":
        # columns = [_news_carousel(entry) for entry in feature_utils.google_news()]

        # # Carousel template is accepted until 5 columns.
        # # See https://devdocs.line.me/ja/#template-message
        # columns = [c for c in columns if c is not None][:5]

        # carousel_template_message = TemplateSendMessage(
        #     alt_text="Berita hari ini \n Pesan tidak dapat dilihat",
        #     template=CarouselTemplate(columns=columns)
        # )
        # line_bot_api.reply_message(event.reply_token, carousel_template_message)