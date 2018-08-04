

from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
)

from utility import line_bot_api

aimode = False
helptext = """
=== TROMBOSIT ASSISTANCE ===
| /help
| /creator
| /aimode (on/off)
============================
"""


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
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="A person that hate Mandarin much, and hate writing 37 messages"))
    return

# /aimode off
def aimodeoff(event):
    msg = event.message.text
    if msg == "/aimode off":
        global aimode
        aimode = False

# /aimode on       
def aimodeon(event):
    msg = event.message.text
    if msg == "/aimode on":
        global aimode
        aimode = True

def aireply(event):
    msg = event.message.text
    global aimode
    if aimode:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))


