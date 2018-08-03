from . import line_bot_api

from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
)

import Utils


def chatbot(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Apa lu kntl! test message berbeda")
    )


def chatbot2():
    print("hi")