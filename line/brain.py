import os
import google.generativeai as genai

# 直接從環境變數讀取 Key (Render 已設定)
MY_GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=MY_GEMINI_KEY)

def get_ai_response(user_query):
    # 智慧路徑 (保持我們修正好的)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")

    knowledge_context = ""
    if not os.path.exists(docs_path):
        return f"錯誤：找不到知識庫資料夾 {docs_path}"

    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                knowledge_context += f.read() + "\n\n"

    # 設定 AI 模型 (這是 1.5 Flash 最穩定的呼叫方式)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=f"你是一位健行科技大學的親切助教。請嚴格根據以下提供的校園規章回答問題：\n{knowledge_context}\n如果答案不在文本中，請回答不知道。"
    )

    try:
        response = model.generate_content(user_query)
        return response.text
    except Exception as e:
        return f"發生錯誤：{str(e)}"
