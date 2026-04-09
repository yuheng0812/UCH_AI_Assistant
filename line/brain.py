import os
import google.generativeai as genai

# 1. 初始化設定
MY_GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=MY_GEMINI_KEY)

def get_ai_response(user_query):
    # 2. 智慧路徑定位
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")

    knowledge_context = ""
    if not os.path.exists(docs_path):
        return f"【系統訊息】找不到知識庫: {docs_path}"

    try:
        # 只讀取前兩個檔案，避免文本過大導致 404
        count = 0
        for filename in os.listdir(docs_path):
            if filename.endswith(".txt") and count < 3:
                with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                    knowledge_context += f.read() + "\n\n"
                    count += 1
    except Exception as e:
        return f"【系統訊息】讀取失敗: {str(e)}"

    # 3. 呼叫最強大的穩定版模型 gemini-1.0-pro
    # 這個模型是 Google 歷史最久、最不可能噴 404 的版本
    model = genai.GenerativeModel(model_name="gemini-1.0-pro")

    try:
        # 將指示與問題合併 (這是 1.0 版最穩定的做法)
        prompt = f"你是一位健行科大助教。請根據以下校規回答問題：\n{knowledge_context}\n\n問題：{user_query}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 如果還是 404，這裡會噴出具體原因
        return f"【最終Debug】請檢查API Key是否正確。錯誤內容: {str(e)}"
