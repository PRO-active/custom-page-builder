import streamlit as st

# セッション状態を初期化
if 'sections' not in st.session_state:
    st.session_state.sections = []

def add_section():
    st.session_state.sections.append({'title': '', 'content': ''})

def remove_section(index):
    st.session_state.sections.pop(index)

def update_section(index, title, content):
    st.session_state.sections[index]['title'] = title
    st.session_state.sections[index]['content'] = content

def generate_html():
    html = "<html><head><title>My Custom Page</title></head><body>"
    for section in st.session_state.sections:
        html += f"<div style='padding: 20px;'>"
        html += f"<h2>{section['title']}</h2>"
        html += f"<p>{section['content']}</p>"
        html += "</div>"
    html += "</body></html>"
    return html

# アプリの名前と説明
st.title("My Custom Page Builder")
st.write("このアプリを使って、オリジナルのウェブページを簡単に作成できます。")

st.header("セクションの設定")

# セクション追加ボタン
if st.button("セクションを追加"):
    add_section()

# セクションの表示
for index, section in enumerate(st.session_state.sections):
    title = st.text_input(f"セクション {index+1} のタイトル", section['title'], key=f"title_{index}")
    content = st.text_area(f"セクション {index+1} の内容", section['content'], key=f"content_{index}")
    st.session_state.sections[index]['title'] = title
    st.session_state.sections[index]['content'] = content
    if st.button(f"セクション {index+1} を削除", key=f"remove_{index}"):
        remove_section(index)

# ページ生成ボタン
if st.button("ページを生成"):
    st.markdown("### 生成されたページ")
    for section in st.session_state.sections:
        st.markdown(f"""
        <div style="padding: 20px;">
            <h2>{section['title']}</h2>
            <p>{section['content']}</p>
        </div>
        """, unsafe_allow_html=True)

    # HTMLの生成
    html_content = generate_html()

    # HTMLファイルのダウンロードリンクを表示
    st.download_button(
        label="HTMLをダウンロード",
        data=html_content,
        file_name="custom_page.html",
        mime="text/html"
    )

# サイドバーでプレビュー表示
st.sidebar.title("ページのプレビュー")
for section in st.session_state.sections:
    st.sidebar.markdown(f"""
    <div style="padding: 20px;">
        <h2>{section['title']}</h2>
        <p>{section['content']}</p>
    </div>
    """, unsafe_allow_html=True)
