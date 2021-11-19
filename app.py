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
import os
import pandas as pd

app = Flask(__name__)
line_bot_api = LineBotApi('Yhw5V0DuMqmWNsBsD2qOaAQAcCN6tH8hNnMDL4EySJzV9c4fara9/fP2Q982Cc1726FA/V8u4Nt4ZY9apNz4A/X6zMHGkCWh38zNzlqBaA8vFMsEzb6huWaU4PqXMv7LJJPgeJuyFFnm3bn56d8H0wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('bf87a1994230b40b009a542b1747dc3f')

# 推給你自己 
line_bot_api.push_message('U5eb2d6c5020d6fe62e4f1d1e0f15e406', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))

# 推給某個User
# line_bot_api.push_message('UserID', TextSendMessage(text='(後臺訊息)啟動豆芽探索共學ECHO機器人!'))

def push_aiamenber_csv():

  run_cmd = lambda cmd_lis:[os.popen(i).read() for i in cmd_lis.split('\n')]

  cmd_lis = '''ls
  cp ../aiaMenber.csv .
  git config --global user.email "junew@aiacademy.tw"
  git config --global user.name "junew"
  git add .
  git commit -m'update aia menber csv'
  git push https://junew:a5731370081@gitlab.aiacademy.tw/junew/AIA_chatbot.git
  '''
  os.chdir('AIA_chatbot')
  run_cmd(cmd_lis)
  os.chdir('..')


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

    user_id = event.source.user_id # 哪一個使用者傳的訊息
    profile = line_bot_api.get_profile(user_id) # 取得使用者個人資料
    user_name = profile.display_name # 他的帳號名稱

    global df
    global key
    
    
    if key == '註冊' and event.message.text.isdigit():
        msg = '收到您的卡號，幫您註冊...'
        line_bot_api.push_message(user_id, TextSendMessage(text=msg)) 
        
        if user_name in df.profileName.values:
            index = df['profileName'] == user_name
            df.loc[index, 'card'] = str(event.message.text)
            msg += str(df.loc[index, :].values[0])
        else:
            lis = [user_name, str(event.message.text)]
            df.loc[len(df)] = lis
            msg += str(lis)

        line_bot_api.push_message(user_id, TextSendMessage(text=msg)) 
        key = None
    elif event.message.text == '註冊':
        msg = '為您註冊資料庫，請輸入(更新)卡號...'
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
        key = '註冊'
    
    if event.message.text == '我的卡號':
        key = '我的卡號'
    if key == '我的卡號':
        if user_name in df.profileName.values:
            user_card = df[df['profileName'] == user_name]['card'].values[0]
            msg = user_name+':'+str(user_card)
            line_bot_api.push_message(user_id, TextSendMessage(text=msg)) 
            key = None
    


    if event.message.text == 'hit':
        msg = '請稍等，為您聯繫資料庫確認打卡資訊...，'
        line_bot_api.push_message(user_id,
          TextSendMessage(text=msg)) 

        if user_name in df['profileName'].values:
            index = df[df['profileName'] == user_name]
            user_card = df[df['profileName'] == user_name]['card'].values[0]
        
            result = os.popen("curl -X POST 'https://class.aiacademy.tw/enter_logs/ajax_logs2.php'\
              --data-raw 'room_id=17&card_id={user_card}&bye=F'".format(user_card=user_card)).read()

            a = result.split("data")[1]
            b = a.split(':')[2].split(',')[0]
            b = b[1:-1]
            d = bytes(b, encoding='utf-8')

            if str(d.decode('unicode_escape')) == str(user_card):
                msg = '打卡失敗，卡號錯誤...你目前註冊的卡號是{user_card}'.format(user_card=user_card)
            else:
                msg = d.decode('unicode_escape')+'打卡成功'
            line_bot_api.push_message(user_id, TextSendMessage(text=msg)) 
        else:
            msg = '你尚未註冊卡號'
            line_bot_api.push_message(user_id,
              TextSendMessage(text=msg)) 
    else:
      pass
    
    
    df_origin = pd.read_csv('aiaMenber.csv')
    df_origin.loc[:,'card'] = df_origin.card.astype(object)
    length_diff = df.merge(df_origin,indicator = True, how='left').loc[lambda x : x['_merge']!='both'].shape[0]
    if length_diff > 0:
      df.to_csv('aiaMenber.csv', index=False)
      push_aiamenber_csv()


if __name__ == "__main__":
    os.system('git clone https://junew:a5731370081@gitlab.aiacademy.tw/junew/AIA_chatbot.git')
    try:
      df = pd.read_csv('AIA_chatbot/aiaMenber.csv')
      df.to_csv('aiaMenber.csv', index=False)
    except FileNotFoundError:
      df = pd.DataFrame([], columns=['profileName', 'card'])
      df.to_csv('aiaMenber.csv', index=False)

    key = None
    # run_webApi()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
