import os
from pathlib import Path
import streamlit as st

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
# サイドバー
# ============================================================
with st.sidebar:
    st.title("⚔️ 参謀本部 S v2")
    st.caption("Strategic Intelligence for Excellency")
    st.divider()
    
    st.success("🟢 システム起動完了")
    st.info("APIキーなしで操作モード実行中")
    
    mode = st.radio(
        "実行モード選択",
        ["1. 自由対話・通常質問", "2. 自律型戦略分析", "3. 機密・ローカル資料分析"]
    )
    
    st.divider()
    if st.button("💬 対話履歴をクリア"):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# メイン画面 (UI)
# ============================================================
st.markdown("<div class='main-title'>STRATEGIC INTELLIGENCE S</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>〜 閣下の御意思決定を助ける最高参謀AI 〜</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "はっ、閣下！参謀AI「S」のインターフェース起動が完了いたしました。ご命令をどうぞ。"}
    ]

for msg in st.session_state.messages:
    avatar = "⚔️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 対話入力
if mode == "1. 自由対話・通常質問":
    if user_input := st.chat_input("閣下、ご指示を入力してください..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="⚔️"):
            reply = f"はっ、閣下！「{user_input}」とのご指示、拝受いたしました。只今システム疎通の最終確認中でございます。"
            st.write(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})
