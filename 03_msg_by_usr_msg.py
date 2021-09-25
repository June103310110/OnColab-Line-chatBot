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

line_bot_api = LineBotApi('Channel access token')
handler = WebhookHandler('Channel secret')

# 推給你自己 
line_bot_api.push_message('Your user ID ', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))

# 推給某個User
# line_bot_api.push_message('UserID', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))


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
    
    reply_msg = event.message.text+'\nyour User ID is '+user_id+\
                    ' \n輸入「你好」會啟動reply_message回復「不錯喔」，\
                    \n輸入「發訊息給我」會啟動push_message由機器人主動發訊息給使用者，\
                    \n輸入「我是誰」會調用get_profile取得身分並回覆使用者訊息'
    
    if event.message.text=='你好':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='不錯喔'))
    if event.message.text=='發訊息給我':
        line_bot_api.push_message(
           user_id,
           TextSendMessage(text='這個訊息是基於ID主動發出的(push_message)'))
    if event.message.text=='我是誰':
        profile = line_bot_api.get_profile(user_id)
        msg_ = '你的帳號是: '+ profile.display_name + '\n你的ID是: '+profile.user_id+'\n你的大頭貼網址是: '\
                    +profile.picture_url+'\n你的使用者自介內容是: '+profile.status_message
        line_bot_api.push_message(
             user_id,
             TextSendMessage(text=msg_))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
