import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# 1. 初始化
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_ai_response(user_query):
    # 先把使用者輸入的空白去掉
    query_stripped = user_query.strip()
    
    # ======= 🌟 核心功能：自動偵測使用者是不是「貼網址」 =======
    if query_stripped.startswith("http://") or query_stripped.startswith("https://"):
        url = query_stripped
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        try:
            # 現場對使用者貼的網址發送爬蟲連線
            response = requests.get(url, headers=headers, timeout=8)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                raw_text = soup.get_text()
                # 清洗網頁雜訊文字
                clean_lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
                web_context = "\n".join(clean_lines)
                
                # 餵給 Gemini 模型
                model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
                prompt = f"你是一位健行科大 AI 助手。使用者剛剛提供了一個網頁網址，以下是該網頁的即時抓取內容：\n\n{web_context}\n\n請根據上方網頁內容，用親切的口吻向使用者簡單摘要這個網頁的重點，並告訴他你已經學會這頁的資訊了！"
                
                response_ai = model.generate_content(prompt)
                return f"🌐【網頁爬蟲成功】\n系統已即時載入該網址資訊！摘要如下：\n\n{response_ai.text}"
            else:
                return f"❌【爬蟲失敗】無法讀取該網頁，錯誤代碼：{response.status_code}"
        except Exception as e:
            return f"❌【連線異常】無法存取該網址，原因：{str(e)}"
            
    # ======= 🏫 原本的功能：使用者問一般問題，讀取本地校規 =======
    # 2. 定位校規
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, "..", "docs")
    
    knowledge_context = ""
    if os.path.exists(docs_path):
        for filename in os.listdir(docs_path):
            if filename.endswith(".txt"):
                with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                    knowledge_context += f.read() + "\n\n"
                    
    # 3. 使用模型名稱
    model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
    
    # 4. 組合問題
    prompt = f"你是一位健行科大助教。請根據以下校規回答問題：\n{knowledge_context}\n\n問題：{user_query}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"【連線訊息】{str(e)}"
