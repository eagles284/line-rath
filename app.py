# mybot/app.py
import os
from decouple import config
from flask import (
    Flask, request, abort, render_template, url_for
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from utility import (
    handler, app, line_bot_api
)
import chatfeatures

@app.route('/math', methods=['GET', 'POST'])
def math(): 
    return render_template('math.html')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)


    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)


    return 'OK'

# FEATURES
aifeatures = [
    chatfeatures.help,
    chatfeatures.creator,
    chatfeatures.love,
    chatfeatures.wiki,
    chatfeatures.grafik,
    chatfeatures.aimodeoff,
    chatfeatures.aimodeon,
    chatfeatures.aireply
]

# ON MESSAGE RECEIVED: GROUP OR PERSONAL
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    for feature in aifeatures:
        feature(event)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)