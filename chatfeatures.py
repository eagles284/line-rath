

from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
)

from utility import line_bot_api

helptext = """

=== TROMBOSIT ASSISTANCE ===
| /help
| /creator
| /aimode
============================

"""

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
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=helptext))
    return

# /creator
def creator(event):
    msg = event.message.text
    if msg == "/creator":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="A person that hate Mandarin much, and hate writing 37 messages"))
    return

# /chatbot off
def chatbot(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


