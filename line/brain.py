import os
import google.generativeai as genai

# =================================================
# 【測試專用】直接在這裡填入你剛申請的新 API Key
TEST_KEY = "AIzaSyCo4Cw_LRQLRd5tw6dd3F8GfcpSHN_mBpE"
# =================================================

genai.configure(api_key=TEST_KEY)

def get_ai_response(user_query):
    # 這裡我們完全不讀取 docs，直接問 Google 一個簡單的問題
    # 如果這個能成功回話，就代表你的 Key 跟連線是 100% 沒問題的
    
    try:
        # 使用最基礎的模型
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 測試連線的指令
        test_prompt = f"這是一個API測試。請簡短回覆我：'連線成功，我收到你的問題了：{user_query}'"
        
        response = model.generate_content(test_prompt)
        
        # 如果成功，回傳 AI 的話
        return f"✅【測試成功】\nAI 回應：{response.text}"
        
    except Exception as e:
        # 如果失敗，回傳最詳細的報錯內容
        return f"❌【測試失敗】\n報錯內容：{str(e)}"
