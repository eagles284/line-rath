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



aimode = False
helptext = """====== TROMBOSIT HELP ======
||  /help
||  /creator
||  /aimode (on/off)
||  /love (orang1, orang2)
||  /wikipedia (search...)
||  /grafik (ax+by=c)
============================"""


def textreply(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

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

# /help
def help(event):
    msg = event.message.text
    if msg == "/help":
        textreply(event, helptext)
    return


# /creator
def creator(event):
    msg = event.message.text
    if msg == "/creator":
        textreply(event, "A man who hates Mandarin very much. I hope you know what I mean :)")
    return

# /aimode off
def aimodeoff(event):
    msg = event.message.text
    if msg == "/aimode off":
        global aimode
        aimode = False
        textreply(event, "AI mode off")

# /aimode on       
def aimodeon(event):
    msg = event.message.text
    if msg == "/aimode on":
        global aimode
        aimode = True
        textreply(event, "AI mode on")

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

def grafik(event):
    msg = str(event.message.text)
    if msg.startswith("/grafik"):

        # feature_utils.plot()
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url='https://trombosit.herokuapp.com/math.png',
                preview_image_url='https://trombosit.herokuapp.com/math.png'
            ))


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