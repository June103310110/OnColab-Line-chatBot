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

line_bot_api = LineBotApi('F3wxw5f1SzY7d5DgxkJPwW5qdVWI/iDCZ0+Kj/OHvrviNYBd2WH+qm8rLANu/x/xsLXRijx5qR/NTDfBrCJtukltAum5r3SP2hX5ClN8A671UjlUiqisf1SlaWH4Wom1FKibFtLcdV4rLyzK0aZSmQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c220d0e085bf26cf5dba48f2eccf928e')

# 推給你自己 
line_bot_api.push_message('U5eb2d6c5020d6fe62e4f1d1e0f15e406', TextSendMessage(text='歡迎使用豆芽探索共學ECHO機器人'))
# 推給某個User
# line_bot_api.push_message('UserID', TextSendMessage(text='歡迎使用豆芽探索共學ECHO機器人'))


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
      # get user id when reply
    user_id = event.source.user_id
    print("user_id =", user_id)
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text+'your User ID is'+user_id))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
