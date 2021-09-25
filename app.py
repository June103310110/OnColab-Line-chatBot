from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, Video, ExternalLink
)

# from linebot.models import ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea
from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
app = Flask(__name__)

line_bot_api = LineBotApi('F3wxw5f1SzY7d5DgxkJPwW5qdVWI/iDCZ0+Kj/OHvrviNYBd2WH+qm8rLANu/x/xsLXRijx5qR/NTDfBrCJtukltAum5r3SP2hX5ClN8A671UjlUiqisf1SlaWH4Wom1FKibFtLcdV4rLyzK0aZSmQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c220d0e085bf26cf5dba48f2eccf928e')

# 推給你自己 
line_bot_api.push_message('U5eb2d6c5020d6fe62e4f1d1e0f15e406', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))
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


button_template_message =ButtonsTemplate(
                        thumbnail_image_url="https://i.imgur.com/d3vfgZP.png",
                        title='Menu', 
                        text='Please select',
                        ratio="1.51:1",
                        image_size="cover",
                        actions=[
#                                PostbackTemplateAction 點擊選項後，
#                                 除了文字會顯示在聊天室中，
#                                 還回傳data中的資料，可
#                                 此類透過 Postback event 處理。
#                             PostbackTemplateAction(
#                                 label='postback 回發訊息data參數會被回傳到', 
#                                 text='postback text',
#                                 data='action=buy&itemid=1'
#                             ),
                            MessageTemplateAction(
                                label='message會回傳你好', text='你好'
                            ),
                            URITemplateAction(
                                label='uri可回傳網址', uri='https://hackmd.io/DPLQVfzFS3yAs4ZcpY56NQ?view'
                            )
                        ]
                    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
      # get user id when reply
    user_id = event.source.user_id
    print("user_id =", user_id)
    
    reply_msg = event.message.text+'\nyour User ID is '+user_id+\
                    ' \n輸入「你好」會啟動reply_message回復「不錯喔」'
    
    if event.message.text=='你好':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='不錯喔'))
        
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg))
        try:
    #     alt_text 因template只能夠在手機上顯示，因此在PC版會使用alt_Text替代
            line_bot_api.push_message(user_id, TemplateSendMessage(alt_text="Template Example", 
                                                                   template=button_template_message))
        except LineBotApiError as e:
            # error handle
            raise e

        
        

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
