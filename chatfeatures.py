from random import randint
from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
)
from utility import line_bot_api
import feature_chatai
import feature_utils


aimode = False
helptext = """====== TROMBOSIT HELP ======
||  /help
||  /creator
||  /aimode (on/off)
||  /love (orang1, orang2)
||  /wikipedia (search...)
============================"""


def textreply(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

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
        textreply(event, "A person that hates Mandarin and writing 37 messages. I hope you know what i mean :)")
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


