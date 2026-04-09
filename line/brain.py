import os
import google.generativeai as genai

# 1. 初始化設定 (強制使用穩定通道)
MY_GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=MY_GEMINI_KEY)

def get_ai_response(user_query):
    # 2. 智慧路徑定位
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")

    knowledge_context = ""
    if not os.path.exists(docs_path):
        return f"【系統訊息】找不到知識庫資料夾: {docs_path}"

    try:
        for filename in os.listdir(docs_path):
            if filename.endswith(".txt"):
                with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                    knowledge_context += f.read() + "\n\n"
    except Exception as e:
        return f"【系統訊息】讀取檔案失敗: {str(e)}"

    # 3. 呼叫模型 (使用最穩定的 1.5-flash)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=f"你是一位健行科技大學的親切助教。請根據以下規章回答問題：\n{knowledge_context}"
    )

    try:
        response = model.generate_content(user_query)
        # 在答案前面加一個星號，讓我們知道這是「新版程式」回的
        return f"✨ {response.text}"
    except Exception as e:
        # 如果還是錯，把錯誤訊息噴出來，方便我們 debug
        return f"【Debug訊息】錯誤內容: {str(e)}"
