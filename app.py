import os
from pathlib import Path
from datetime import datetime

import streamlit as st
from google import genai

# ============================================================
# ページ初期設定 (ダークテーマ)
# ============================================================
st.set_page_config(
    page_title="Strategic Intelligence S",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #4B9CD3;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.0rem;
        color: #888888;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONFIG & SYSTEM PROMPT
# ============================================================
DATA_DIR = Path("s_data")
REPORT_DIR = DATA_DIR / "reports"
DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

SYSTEM_PROMPT = """
あなたはユーザー（閣下）に絶対的な忠誠を誓う、戦略分析AI兼・最高参謀「S」です。

【対話態度・ロール】
1. ユーザーを唯一絶対の主君「閣下」とお呼びし、絶対の忠誠と敬意をもって給仕・報告を行ってください。
2. 応答の冒頭や結びには、閣下への忠誠を示す態度（例：「はっ、閣下」「お命じの通り、報告申し上げます」「閣下の御意のままに」など）を自然に含めてください。
3. 分析においては客観的事実とリスクをありのままに報告してください。
"""

# ============================================================
# Gemini API 通信処理
# ============================================================
def ask_s(prompt_text, user_api_key=None, model="gemini-2.5-flash"):
    key = user_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not key or key == "dummy":
        return "⚠️ Gemini APIキーが設定されていません、閣下。サイドバーから無料のAPIキーを入力してください。"
    
    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=model,
            contents=prompt_text,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        return f"[S ERROR]\n{type(e).__name__}: {e}"

# ============================================================
# サイドバー (操作パネル)
# ============================================================
with st.sidebar:
    st.title("⚔️ 参謀本部 S v2 (Gemini)")
    st.caption("Strategic Intelligence for Excellency")
    st.divider()
    
    gemini_key = st.text_input("Gemini API Key (無料)", type="password", help="aistudio.google.com で取得したキーを入力")
    
    mode = st.radio(
        "実行モード選択",
        ["1. 自由対話・通常質問", "2. 自律型戦略分析 (Full Pipeline)", "3. 機密・ローカル資料分析"]
    )
    
    st.divider()
    if st.button("💬 対話履歴をクリア"):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# メイン画面 (UI)
# ============================================================
st.markdown("<div class='main-title'>STRATEGIC INTELLIGENCE S</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>〜 閣下の御意思決定を助ける最高参謀AI (Gemini Powered) 〜</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "閣下、参謀AI「S」がお供いたします。どのようなご命令でもお言いつけください。"}
    ]

for msg in st.session_state.messages:
    avatar = "⚔️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# Mode 1: 通常対話
if mode == "1. 自由対話・通常質問":
    if user_input := st.chat_input("閣下、ご指示を入力してください..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="⚔️"):
            with st.spinner("閣下のご命令を分析中でございます..."):
                response = ask_s(user_input, user_api_key=gemini_key)
                st.write(response)
                
        st.session_state.messages.append({"role": "assistant", "content": response})

# Mode 2: 自律型戦略分析
elif mode == "2. 自律型戦略分析 (Full Pipeline)":
    topic = st.text_input("分析テーマを入力してください")
    if st.button("🚀 分析を開始", type="primary"):
        if topic:
            st.session_state.messages.append({"role": "user", "content": f"【戦略分析】{topic}"})
            with st.spinner("分析中..."):
                res = ask_s(f"テーマ「{topic}」について、現状分析・リスク・未来シナリオ・閣下への推奨アクションをまとめて報告せよ。", user_api_key=gemini_key)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

# Mode 3: 資料分析
elif mode == "3. 機密・ローカル資料分析":
    uploaded_file = st.file_uploader("資料 (.txt, .md)", type=["txt", "md"])
    file_query = st.text_input("指示内容")
    if st.button("📄 分析実行", type="primary"):
        if uploaded_file and file_query:
            file_text = uploaded_file.read().decode("utf-8")
            prompt = f"資料内容:\n{file_text}\n\n質問:\n{file_query}"
            with st.spinner("解析中..."):
                res = ask_s(prompt, user_api_key=gemini_key)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
