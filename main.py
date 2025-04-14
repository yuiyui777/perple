import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# APIキーの存在チェック
YOUR_API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not YOUR_API_KEY:
    st.error("エラー: PERPLEXITY_API_KEYが設定されていません。.envファイルを確認してください。")
    st.stop()

# -------------------------------
# API クライアントの設定
# -------------------------------
client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# -------------------------------
# サイドバーのレイアウト設定
# -------------------------------
st.sidebar.title("業界情報調査アプリ")
st.sidebar.markdown(
    """
    このアプリでは、最新の業界情報を Perplexity API から取得して表示します。  
    以下の選択肢から調査対象の業界と、情報の詳細度を選んでください。
    """
)

# 業界選択のドロップダウン
industry = st.sidebar.selectbox("業界を選択", 
                                ["IT", "小売", "製造", "金融", "ヘルスケア","ガス"])

# 情報詳細度のラジオボタン
info_level = st.sidebar.radio("情報の詳細度", ("概要", "詳細","小学生が分かる粒度"))

# -------------------------------
# メイン画面の設定
# -------------------------------
st.title("業界情報調査アプリ")
st.write("選択された業界の最新情報を表示します。")
st.write(f"**業界:** {industry}")
st.write(f"**情報の詳細度:** {info_level}")

# -------------------------------
# Perplexity API 呼び出し関数
# -------------------------------
def query_perplexity(industry, level):
    # API に渡すメッセージの定義（システムとユーザーメッセージ）
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": (
                f"{industry} 業界について、{level}な情報を教えてください。"
            ),
        },
    ]
    
    try:
        # チャット完了（ストリーミングなし）の呼び出し
        response = client.chat.completions.create(
            model="sonar",
            messages=messages,
        )
        return response
    except Exception as e:
        st.error(f"API呼び出し中にエラーが発生しました: {str(e)}")
        return None

# -------------------------------
# API 呼び出しボタン
# -------------------------------
if st.button("情報を取得"):
    st.info("情報を取得中です...")
    result = query_perplexity(industry, info_level)
    
    if result is None:
        st.error("情報の取得に失敗しました。")
    else:
        # レスポンスの表示
        st.subheader("取得した情報")
        st.write(result)
