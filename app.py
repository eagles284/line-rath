# mybot/app.py
import os
from decouple import config
from flask import (
    Flask, request, abort, render_template, url_for, send_from_directory,
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage,
)
from utility import (
    handler, app, line_bot_api
)
import chatfeatures
from OpenSSL import SSL

# sslify = SSLify(app)

@app.route('/rout/<path:path>')
def static_file(path):
    return app.send_static_file('rout/'+path)

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
    chatfeatures.log,
    chatfeatures.phrases,
    chatfeatures.help,
    chatfeatures.push,
    chatfeatures.creator,
    chatfeatures.love,
    chatfeatures.wiki,
    chatfeatures.grafik,
    chatfeatures.webss,
    chatfeatures.absen,
    chatfeatures.chess,
    chatfeatures.checkuserid,
    chatfeatures.aimodeon,
    chatfeatures.aireply
]

imgfeatures = [
    chatfeatures.img,
]

# ON MESSAGE RECEIVED: GROUP OR PERSONAL
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):

    for feature in aifeatures:
        feature(event)

# ON IMAGE RECEIVED: GROUP OR PERSONAL
@handler.add(MessageEvent, message=ImageMessage)
def handle_text_message(event):

    for feature in imgfeatures:
        feature(event)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    context = ('/etc/letsencrypt/csr/0002_csr-certbot.pem', '/etc/letsencrypt/keys/0002_key-certbot.pem')
    app.run(host='0.0.0.0', port=port, threaded=True, debug=True, ssl_context=('fullchain.pem', 'privkey.pem'))