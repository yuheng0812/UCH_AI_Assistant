from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

# 💡 關鍵：引入你之前寫好的 RAG 大腦邏輯
from brain import get_ai_response 

app = Flask(__name__)

# ⚠️ 請填入你剛才在 LINE 後台拿到的資訊
LINE_CHANNEL_ACCESS_TOKEN = 'jOdN0dT28JLd0d18ukpQxml2xdX3yqexeQW/VFPt4YvTtuoIljasEDrNjobhkHOJRLOB/xHJhsbbl8ysoFV72Yx4uGsBRQDJzG4L1nZaR6kY16bA4H790FSI0xwHSUyotTxIH+tN2sa0hr/zcOhaqQdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = '0c113131e53f023d01c5b652a0c53331'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 接收 LINE 訊息的入口
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理文字訊息的邏輯
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 1. 取得使用者在 LINE 傳來的文字
    user_text = event.message.text
    print(f"收到 LINE 訊息: {user_text}")

    # 2. 丟給 brain.py 的大腦去翻書並問 Gemini
    ai_reply = get_ai_response(user_text)

    # 3. 將 AI 的回答傳回給使用者的 LINE 手機
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_reply)
    )

if __name__ == "__main__":
    # Line Bot 預設跑在 5000 埠口
    app.run(port=5000)