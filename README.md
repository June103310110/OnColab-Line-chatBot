# heroku-chatBot

### 如何使用colab測試Line chatbot
```
!pip install flask
!pip install line-bot-sdk
!pip install pyngrok
```
https://colab.research.google.com/drive/1WA8uW7230He77jyzZcS6ijVLPj64cBid?hl=zh-tw#scrollTo=YIidv3tARHmg
> 執行後要記得去[Line developer中心](https://developers.line.biz/console/)調整Webhook URL，調整成Colab吐出來的頁面連結。(範例code要加/callback，e.g.`https://31e0-35-231-164-122.ngrok.io/callback`)
> 很麻煩的是每次測試都要調整一次Webhook URL，因為ngrok的位址不是固定的


- 按鈕範例
  - [ngrok_chatbot_Buttom_template.ipynb](https://colab.research.google.com/drive/10yLAzSwmJaXKhlypA0__dDdxZs-qaZf6?hl=zh-tw#scrollTo=Lmazs04mRIQl)
