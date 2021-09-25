from flask import Flask, request, abort
import string
from flask import url_for, render_template 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, Video, ExternalLink, PostbackEvent
)

# from linebot.models import ImagemapSendMessage, BaseSize, URIImagemapAction, MessageImagemapAction, ImagemapArea
from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction
import random
import glob
import os

try:
    os.makedirs('./static/user_upload', exist_ok=False)
    os.makedirs('./templates', exist_ok=False)
except FileExistsError:
    pass
    
app = Flask(__name__)
PEOPLE_FOLDER = os.path.join('static', 'user_upload')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

# 設定chatbot
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
                            MessageTemplateAction(
                                label='message會回傳你好', text='你好'
                            ),
                            URITemplateAction(
                                label='uri可回傳網址', uri='https://hackmd.io/DPLQVfzFS3yAs4ZcpY56NQ?view'
                            )
                        ]
                    )

# 取得使用者上傳的圖片
@handler.add(MessageEvent)
def handle_img_message(event):
    
    user_id = event.source.user_id
    print("user_id =", user_id)
    print(event.message.type)
    if event.message.type=='image':
        image_name = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(4))
        image_content = line_bot_api.get_message_content(event.message.id)
        image_name = image_name.upper()+'.jpg'
        path='./static/user_upload/'+user_id+'_'+image_name
        print(path)
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='收到照片，分析中!'))

                

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
      # get user id when reply
    user_id = event.source.user_id
    print("user_id =", user_id)
    print(event.message.type)
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
