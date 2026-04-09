import os
from google import genai
# 如果沒有安裝 python-dotenv，可以先註解掉下面這行
# from dotenv import load_dotenv 

# 1. 直接在這裡貼上你的 API Key (最保險的做法)
MY_GEMINI_KEY = "AIzaSyAEmsIsBwr208r7VU2JVo71mQfwQED6qA8" 

# 2. 初始化 Gemini 客戶端
client = genai.Client(api_key=MY_GEMINI_KEY)

def get_ai_response(user_query):
    # 3. 讀取知識庫 (修正路徑確保讀得到)
    knowledge_context = ""
    # 這裡的路徑請根據你 docs 資料夾的位置調整，如果 docs 在 src 裡面就寫 "src/docs"
    # 取得 brain.py 檔案所在的目錄 (即 /line 資料夾)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # 往上一層找 docs 資料夾
    docs_path = os.path.join(base_dir, "..", "docs")
    
    if not os.path.exists(docs_path):
        return f"錯誤：找不到知識庫資料夾 {docs_path}"

    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            with open(os.path.join(docs_path, filename), "r", encoding="utf-8") as f:
                knowledge_context += f.read() + "\n\n"

    # 4. 設定指令
    system_instruction = f"""
    你是一位健行科技大學的親切助教。
    請嚴格根據以下提供的校園規章文本回答問題：
    {knowledge_context}
    
    如果問題在文本中找不到答案，請回答不知道。
    """

    # 5. 產生回答
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash-8b",
            config={"system_instruction": system_instruction},
            contents=user_query
        )
        return response.text
    except Exception as e:
        return f"發生錯誤：{str(e)}"
