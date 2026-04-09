import os
import google.generativeai as genai

# 1. 初始化設定 (從 Render 環境變數讀取新 Key)
MY_GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=MY_GEMINI_KEY)

def get_ai_response(user_query):
    # 2. 定位校規知識庫 (從 /line 往上一層找 /docs)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")

    knowledge_context = ""
    if not os.path.exists(docs_path):
        return f"【系統錯誤】找不到知識庫資料夾，請檢查路徑。"

    try:
        # 讀取 docs 資料夾內所有校規文字檔
        for filename in os.listdir(docs_path):
            if filename.endswith(".txt"):
                with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                    knowledge_context += f.read() + "\n\n"
    except Exception as e:
        return f"【系統錯誤】讀取校規失敗: {str(e)}"

    # 3. 建立模型 (使用最穩定的 1.5-flash)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 4. 組合最終指令 (不使用 system_instruction 參數，避免觸發 404 錯誤)
    # 我們把助教身分和校規直接包進 Prompt 裡面
    full_prompt = f"""你是一位健行科技大學的親切助教。
請嚴格根據以下提供的校園規章文本回答問題。
如果答案不在文本中，請回答不知道。

【校園規章文本開始】
{knowledge_context}
【校園規章文本結束】

學生提出的問題：{user_query}
"""

    try:
        # 5. 產生回答
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        # 如果還是失敗，會噴出具體錯誤訊息
        return f"【連線訊息】請確認金鑰是否已更新。錯誤內容: {str(e)}"
