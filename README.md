# OnColab-chatBot 
#### Readme這邊都是colab連結，如果要部屬到gcp/heroku請用上面的程式碼
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
  - [ngrok_chatbot_Buttom_template_V2.ipynb](https://colab.research.google.com/drive/1N_HBu17HyQLwNsHDuEeAkS9QAOH85Ydy?usp=sharing)
- 減肥
  - [範例連結](https://colab.research.google.com/drive/1IVuyqkquDfJkwFoOtATVAXYtZS_F-Tlk?hl=zh-tw#scrollTo=mSi-0mnRRGUm)  
- 吃藥
  - [範例連結](https://colab.research.google.com/drive/1OhgmCpUblTxximffTfmRGx7Ghb6ZjOZQ?hl=zh-tw#scrollTo=Lmazs04mRIQl)
- 回傳圖片
  - [範例連結](https://colab.research.google.com/drive/1Z7Zq2TKwWXRAhsv8WzKN5HKVGNEeN9b6?hl=zh-tw#scrollTo=Lmazs04mRIQl) 
- 瘦身助理
  - [範例連結](https://colab.research.google.com/drive/13k5Ouw2WZMdOx3_xN9qEs_bXjYGaxCXT?hl=zh-tw#scrollTo=CMOocpugWgce)
- V2_瘦身助理_ngrok_chatbot_Buttom_template.ipynb
  - [範例連結](https://colab.research.google.com/drive/1JdluL1yZ_VgXFFexGukBYR_5WiXULqzf?hl=zh-tw#scrollTo=Lmazs04mRIQl) 
- V3_基礎醫療_ngrok_chatbot_Buttom_template.ipynb
  - [範例連結](https://colab.research.google.com/drive/1odesYQtuF2SMnVujMyXmKlJKz62HXW52?hl=zh-tw#scrollTo=Lmazs04mRIQl)
- V1_June_馬偕護專_使用者收入支出.ipynb
  - [範例連結](https://colab.research.google.com/drive/1FaJTsjW-SorDXRQzehIesSA-t2gXU_Ly?hl=en#scrollTo=Lmazs04mRIQl)
- V1_June_馬偕護專_吃藥
  - [範例連結](https://colab.research.google.com/drive/1tecJS_E_shmb0cKcENm_9GLnaxPOP2ML?hl=en#scrollTo=Lmazs04mRIQl)
