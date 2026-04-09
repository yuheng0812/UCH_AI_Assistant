import streamlit as st
from brain import get_ai_response # 引入我們剛寫好的大腦

st.set_page_config(page_title="UCH AI Assistant", layout="centered")
st.title("🎓 健行科大 AI 校園助手")

# 聊天紀錄初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 顯示對話紀錄
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 使用者輸入
if prompt := st.chat_input("有什麼想問助教的嗎？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 呼叫我們的大腦
    with st.chat_message("assistant"):
        response = get_ai_response(prompt) # 直接用 brain.py 的 function
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})