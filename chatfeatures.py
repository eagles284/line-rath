from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
)

from utility import line_bot_api
import feature_chatai


aimode = False
helptext = """====== TROMBOSIT HELP ======
||  /help
||  /creator
||  /aimode (on/off)
||  /love (orang1, orang2)
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
    
def love(event):
    msg = str(event.message.text)
    if msg.startswith("/love"):
        textreply(event, "Calculating love")