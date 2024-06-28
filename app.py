import streamlit as st

# ユーザーインターフェースの作成
st.title("オリジナルページ作成アプリ")

st.header("ページの設定")

# 入力フォーム
title = st.text_input("ページのタイトル")
background_color = st.color_picker("背景色を選択", "#ffffff")
text_color = st.color_picker("文字色を選択", "#000000")
content = st.text_area("ページの内容")

# ボタンが押された場合
if st.button("ページを生成"):
    # 生成されたページを表示
    st.markdown(f"""
    <div style="background-color: {background_color}; color: {text_color}; padding: 20px;">
        <h1 style="text-align: center;">{title}</h1>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)

# サイドバー
st.sidebar.title("ページのプレビュー")
st.sidebar.markdown(f"""
    <div style="background-color: {background_color}; color: {text_color}; padding: 20px;">
        <h1 style="text-align: center;">{title}</h1>
        <p>{content}</p>
    </div>
    """, unsafe_allow_html=True)