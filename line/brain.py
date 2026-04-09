import os
import google.generativeai as genai

# =================================================
# 1. 直接在這裡貼上你的新 API Key (硬寫進去)
# 請確保這串字夾在引號中間，前後沒有空格
MY_GEMINI_KEY = "AIzaSyCo4Cw_LRQLRd5tw6dd3F8GfcpSHN_mBpE" 
# =================================================

genai.configure(api_key=MY_GEMINI_KEY)

def get_ai_response(user_query):
    # 2. 定位校規路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")

    knowledge_context = ""
    if not os.path.exists(docs_path):
        return f"【系統錯誤】找不到資料夾: {docs_path}"

    try:
        for filename in os.listdir(docs_path):
            if filename.endswith(".txt"):
                with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                    knowledge_context += f.read() + "\n\n"
    except Exception as e:
        return f"【系統錯誤】讀取失敗: {str(e)}"

    # 3. 建立模型 (使用最穩定的字串，不帶任何參數)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 4. 把所有指示直接寫在 Prompt 裡
    full_prompt = f"你是一位健行科大助教。請根據校規回答問題：\n{knowledge_context}\n\n學生問：{user_query}"

    try:
        # 5. 執行生成
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # 如果這樣還報錯，我們就能看到最真實的錯誤原因
        return f"【Debug連線訊息】{str(e)}"
