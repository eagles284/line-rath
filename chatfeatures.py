

from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
)

from utility import line_bot_api

def customresponse(event):
    msg = event.message.text
    if msg.startswith('arya'):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Apa lo manggil nama gue?"))
    return

def chatbot(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


