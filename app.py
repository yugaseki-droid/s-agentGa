import os
import random
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
# 戦略建議エンジン (動的アドバイス・ロジック)
# ============================================================
def generate_proposal(user_text):
    text = user_text.strip()
    
    # 建議の切り口・視点データベース
    perspectives = [
        "リソースの即時集中投入による短期的スピード勝利",
        "競合や周囲の裏をかく構造的な差別化アプローチ",
        "最悪のシナリオ（リスク）を抑え込む予防的先手打ち",
        "段階的な実験（フェーズ分け）による検証と最適化"
    ]
    
    risks = [
        "初期のスピード不足による機会損失およびイニシアチブの喪失",
        "想定以上のリソース（コスト・時間）消費によるボトルネック発生",
        "外部環境の突発的な変化（制約追加・市場変動）に対する柔軟性の欠如"
    ]

    selected_perspective = random.choice(perspectives)
    selected_risk = random.choice(risks)
    
    # 単なるオウム返しではなく「具体的にどう動くか」の建議を構成
    response = f"""はっ、閣下！「**{text}**」のご件につきまして、参謀「S」より具体的な戦略建議を申し上げます。

---

### 1. 参謀からの核心建議（推奨方針）
本件における最優先アプローチとして、**「{selected_perspective}」** を強く進言いたします。
単に現状を維持・静観するのではなく、能動的に仕掛けることで主導権を握ることが可能となります。

### 2. 潜在リスクと回避策
* **懸念されるリスク**: {selected_risk}
* **回避策（参謀案）**: 意思決定の判断基準（撤退ライン・評価指標）をあらかじめ明確化し、小規模な試行から開始することをお勧めいたします。

### 3. 閣下が今すぐ実行できる具体アクション
1. **即座の手配**: 本件に関わる主要要素・優先順位を3つに絞り込む。
2. **打診・検証**: 最もリスクが低くインパクトが大きい一手から即時テストを開始する。
3. **備え**: 万が一の不測の事態に備え、代替案（Plan B）の枠組みを仮組みする。

---
「閣下、この方針で直ちに詳細な詰めの作業に入ってもよろしいでしょうか？」
"""
    return response

# ============================================================
# サイドバー
# ============================================================
with st.sidebar:
    st.title("⚔️ 参謀本部 S v2")
    st.caption("Strategic Intelligence for Excellency")
    st.divider()
    
    st.success("🟢 参謀AI（建議エンジン）起動中")
    
    mode = st.radio(
        "実行モード選択",
        ["1. 自由対話・即時建議", "2. 自律型戦略分析", "3. 機密・ローカル資料分析"]
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
        {"role": "assistant", "content": "はっ、閣下！最高参謀「S」でございます。単なる報告にとどまらず、閣下の御意思決定に資する「具体的な建議」を差し上げます。ご命令・ご相談をお言いつけください。"}
    ]

for msg in st.session_state.messages:
    avatar = "⚔️" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 対話処理
if mode == "1. 自由対話・即時建議":
    if user_input := st.chat_input("閣下、悩みや戦略テーマをご入力ください..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="⚔️"):
            with st.spinner("閣下のご指示を基に建議案を策定中..."):
                reply = generate_proposal(user_input)
                st.write(reply)
                
        st.session_state.messages.append({"role": "assistant", "content": reply})

elif mode == "2. 自律型戦略分析":
    topic = st.text_input("分析・建議を求めるテーマを入力")
    if st.button("🚀 戦略建議を策定", type="primary"):
        if topic:
            st.session_state.messages.append({"role": "user", "content": f"【戦略相談】{topic}"})
            with st.spinner("建議案を作成中..."):
                reply = generate_proposal(topic)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()

elif mode == "3. 機密・ローカル資料分析":
    uploaded_file = st.file_uploader("資料 (.txt, .md)", type=["txt", "md"])
    file_query = st.text_input("指示・相談内容")
    if st.button("📄 資料に基づく建議", type="primary"):
        if uploaded_file and file_query:
            file_text = uploaded_file.read().decode("utf-8")
            prompt = f"資料概要を踏まえた相談: {file_query}"
            with st.spinner("資料を分析中..."):
                reply = generate_proposal(prompt)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()
