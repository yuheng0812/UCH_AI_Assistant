import os
import google.generativeai as genai

# 1. 初始化 (使用硬寫 Key 或環境變數都可以，建議先用環境變數)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_ai_response(user_query):
    # 2. 定位校規
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")

    knowledge_context = ""
    if os.path.exists(docs_path):
        for filename in os.listdir(docs_path):
            if filename.endswith(".txt"):
                with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                    knowledge_context += f.read() + "\n\n"

    # 3. 使用你在 VS Code 實測成功的「完整模型名稱」
    # 這裡必須帶有 models/ 前綴
    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")

    # 4. 組合問題
    prompt = f"你是一位健行科大助教。請根據以下校規回答問題：\n{knowledge_context}\n\n問題：{user_query}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"【連線訊息】{str(e)}"
