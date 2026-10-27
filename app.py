import streamlit as st
from groq import Groq, GroqError

st.set_page_config(page_title="我的 AI 聊天室", page_icon="💬")
st.title("💬 我的 AI 聊天室")

# 金鑰請放在 Streamlit Cloud 的 Secrets，不要寫進程式碼。
try:
    api_key = st.secrets["GROQ_API_KEY"]
except (KeyError, FileNotFoundError):
    st.error("請先在 Streamlit Secrets 設定 GROQ_API_KEY。")
    st.stop()

client = Groq(api_key=api_key)

# 聊天紀錄保留在目前的使用階段。
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("清除對話"):
    st.session_state.messages = []
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("請輸入你的問題……"):
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
        {"role": "system", "content": "你是一位友善的助理，請使用繁體中文回答。"},
        *st.session_state.messages,
        {"role": "user", "content": prompt},
    ]

    with st.chat_message("assistant"):
        try:
            with st.spinner("AI 思考中……"):
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.7,
                    max_completion_tokens=1024,
                )
            answer = completion.choices[0].message.content or ""
            st.markdown(answer)
        except GroqError:
            st.error("請求失敗，請檢查 API 金鑰、模型及 Groq 使用額度。")
        else:
            st.session_state.messages.extend([
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": answer},
            ])
