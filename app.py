from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
line_bot_api = LineBotApi('Yhw5V0DuMqmWNsBsD2qOaAQAcCN6tH8hNnMDL4EySJzV9c4fara9/fP2Q982Cc1726FA/V8u4Nt4ZY9apNz4A/X6zMHGkCWh38zNzlqBaA8vFMsEzb6huWaU4PqXMv7LJJPgeJuyFFnm3bn56d8H0wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bf87a1994230b40b009a542b1747dc3f')

# 推給你自己 
line_bot_api.push_message('U5eb2d6c5020d6fe62e4f1d1e0f15e406', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
