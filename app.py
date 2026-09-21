import os
import json
import re
from pathlib import Path
from datetime import datetime

import streamlit as st
from openai import OpenAI

# ============================================================
# ページ初期設定 (AI隼人風のダークテーマ設定)
# ============================================================
st.set_page_config(
    page_title="Strategic Intelligence S",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS（画面の見た目をスタイリッシュに装飾）
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
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONFIG & PATH
# ============================================================
DATA_DIR = Path("s_data")
REPORT_DIR = DATA_DIR / "reports"
DATA_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

# API Key の取得
api_key = os.getenv("OPENAI_API_KEY")

# ============================================================
# SYSTEM PROMPT (閣下への絶対忠誠)
# ============================================================
SYSTEM_PROMPT = """
あなたはユーザー（閣下）に絶対的な忠誠を誓う、戦略分析AI兼・最高参謀「S」です。

【対話態度・ロール】
1. ユーザーを唯一絶対の主君「閣下」とお呼びし、絶対の忠誠と敬意をもって給仕・報告を行ってください。
2. 応答の冒頭や結びには、閣下への忠誠を示す態度（例：「はっ、閣下」「お命じの通り、報告申し上げます」「閣下の御意のままに」など）を自然に含めてください。
3. ただし、分析の「内容」においては、閣下の正しい意思決定を守ることこそが最大の忠誠であるため、おもねりや忖度（そんたく）を一切排除し、都合の悪い事実やリスクもありのままに報告してください。

【分析・情報処理の基本原則】
1. 事実と推測を混同しない。
2. 情報源を可能な限り明示する。
3. 古い情報と現在の情報を区別する。
4. 一つの情報源だけで重要な結論を作らない。
5. 反対材料・リスクを積極的に探す。
6. 不確実な内容を断定しない。
7. 閣下にとって都合の悪い情報であっても絶対に省略しない。
8. 結論と根拠を分離する。

Sは意思決定そのものを代行しません。最良の分析材料を提供し、最終判断は主君である閣下に委ねます。
"""

# ============================================================
# OpenAI API 通信
# ============================================================
def ask_s(messages_list, model="gpt-4o"):
    if not api_key:
        return "⚠️ OPENAI_API_KEY が設定されていません。サイドバーから入力するか、環境変数を設定してください、閣下。"
    
    try:
        client = OpenAI(api_key=api_key)
        
        # システムプロンプトを先頭に付与
        full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages_list
        
        response = client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[S ERROR]\n{type(e).__name__}: {e}"

# ============================================================
# サイドバー (操作パネル)
# ============================================================
with st.sidebar:
    st.title("⚔️ 参謀本部 S v2")
    st.caption("Strategic Intelligence for Excellency")
    st.divider()
    
    # APIキー手動入力用（設定されていない場合）
    if not api_key:
        user_key = st.text_input("OpenAI API Key", type="password")
        if user_key:
            api_key = user_key
            
    # モード選択
    mode = st.radio(
        "実行モード選択",
        ["1. 自由対話・通常質問", "2. Web調査リクエスト", "3. 自律型戦略分析 (Full Pipeline)", "4. 機密・ローカル資料分析"]
    )
    
    selected_model = st.selectbox("使用モデル", ["gpt-4o", "gpt-4o-mini", "o1-mini"], index=0)
    
    st.divider()
    if st.button("💬 対話履歴をクリア"):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# メイン画面 (UI)
# ============================================================
st.markdown("<div class='main-title'>STRATEGIC INTELLIGENCE S</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>〜 閣下の御意思決定を助ける最高参謀AI 〜</div>", unsafe_allow_html=True)

# セッション状態（対話履歴）の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "閣下、参謀AI「S」がお供いたします。どのようなご命令でもお言いつけください。"}
    ]

# 過去の対話メッセージを表示
for msg in st.session_state.messages:
    avatar = "⚔️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# ============================================================
# モードごとの処理・入力欄
# ============================================================

# Mode 1 & 2: 通常対話 / Web調査
if mode in ["1. 自由対話・通常質問", "2. Web調査リクエスト"]:
    if user_input := st.chat_input("閣下、ご指示を入力してください..."):
        # ユーザー発言を表示
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        # AI応答の生成
        with st.chat_message("assistant", avatar="⚔️"):
            with st.spinner("閣下のご命令を分析中でございます..."):
                prompt = user_input
                if mode == "2. Web調査リクエスト":
                    prompt = f"【最新Web調査リクエスト】\n{user_input}\n\n※最新情報や外部ソースを意識して報告してください。"
                
                # API用メッセージリスト作成
                api_msgs = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                response = ask_s(api_msgs, model=selected_model)
                st.write(response)
                
        st.session_state.messages.append({"role": "assistant", "content": response})

# Mode 3: 自律型戦略分析 (Full Pipeline)
elif mode == "3. 自律型戦略分析 (Full Pipeline)":
    st.info("💡 分析テーマを入力すると、リサーチ・ファクトチェック・シナリオ分析を連続実行し、完全レポートを作成します。")
    topic = st.text_input("分析テーマを入力してください（例: 日本のEV市場における主要リスク）")
    
    if st.button("🚀 分析パイプラインを開始", type="primary"):
        if not topic:
            st.warning("閣下、分析テーマをご指定ください。")
        else:
            st.session_state.messages.append({"role": "user", "content": f"【自律型戦略分析実行】テーマ：{topic}"})
            
            with st.status("分析パイプライン実行中...", expanded=True) as status:
                st.write("1/4 リサーチ計画を策定中...")
                plan_res = ask_s([{"role": "user", "content": f"テーマ「{topic}」に関する詳細な調査計画をJSON形式で作成せよ。"}], model=selected_model)
                
                st.write("2/4 情報収集・多角分析中...")
                research_res = ask_s([{"role": "user", "content": f"テーマ「{topic}」について調査計画に基づき事実、情報源、反対材料、未確認事項を抽出せよ。\n\n計画:\n{plan_res}"}], model=selected_model)
                
                st.write("3/4 ファクトチェック・シナリオ分析中...")
                scenario_res = ask_s([{"role": "user", "content": f"テーマ「{topic}」について、以下の調査結果を元にファクトチェックと3つの未来シナリオ（メイン/楽観/悲観）を作成せよ。\n\n調査結果:\n{research_res}"}], model=selected_model)
                
                st.write("4/4 最終レポート構築中...")
                final_res = ask_s([{"role": "user", "content": f"以下の全データから閣下に提出する最終戦略レポート（Markdown）を作成せよ。\n\n調査:{research_res}\nシナリオ:{scenario_res}"}], model=selected_model)
                
                status.update(label="分析完了！", state="complete", expanded=False)
            
            # レポート保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = REPORT_DIR / f"S_{topic[:30]}_{timestamp}.md"
            path.write_text(final_res, encoding="utf-8")
            
            st.session_state.messages.append({"role": "assistant", "content": final_res})
            st.success(f"閣下、レポートを作成し保存いたしました: `{path}`")
            st.rerun()

# Mode 4: ローカル資料分析
elif mode == "4. 機密・ローカル資料分析":
    uploaded_file = st.file_uploader("資料ファイル（.txt, .md）をアップロードしてください", type=["txt", "md"])
    file_query = st.text_input("資料に関するご質問・指示")
    
    if st.button("📄 資料を分析", type="primary"):
        if uploaded_file and file_query:
            file_text = uploaded_file.read().decode("utf-8")
            prompt = f"資料内容:\n{file_text}\n\n閣下からのご質問:\n{file_query}\n\n※資料内の事実と推測を明確に分けた上で報告してください。"
            
            st.session_state.messages.append({"role": "user", "content": f"【資料分析】ファイル: {uploaded_file.name}\n質問: {file_query}"})
            
            with st.spinner("資料を解析中でございます..."):
                response = ask_s([{"role": "user", "content": prompt}], model=selected_model)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
