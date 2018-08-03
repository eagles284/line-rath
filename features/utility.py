from linebot import (
    LineBotApi, WebhookHandler
)

from flask import Flask, request, abort

app = Flask(__name__)

# Access Token
line_bot_api = LineBotApi('lys1bqOGjTb02EHLeUGXCIQvbnYZpszt523Hpr31Phf7LybqeGEBgfET+mAGGtz97RuEatdMILjc+89BTzanGqKDBfhcPLl2kcwpBZMAUyGyIslfnfoYx0rXbq6bEvM/KsaZX+nfJfpgxr0wk0juXwdB04t89/1O/w1cDnyilFU=')  

# Channel Secret
handler = WebhookHandler('24c03e3674a2407604948e4e96805a03')