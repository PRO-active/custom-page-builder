import streamlit as st
import json
import base64

# セッション状態を初期化
if 'sections' not in st.session_state:
    st.session_state.sections = []

def add_section(section_type='text'):
    section = {'type': section_type, 'title': '', 'content': '', 'order': len(st.session_state.sections)}
    if section_type == 'image':
        section['image'] = None
    st.session_state.sections.append(section)

def remove_section(index):
    st.session_state.sections.pop(index)
    for i, section in enumerate(st.session_state.sections):
        section['order'] = i

def move_section(index, direction):
    if direction == 'up' and index > 0:
        st.session_state.sections[index], st.session_state.sections[index - 1] = st.session_state.sections[index - 1], st.session_state.sections[index]
    elif direction == 'down' and index < len(st.session_state.sections) - 1:
        st.session_state.sections[index], st.session_state.sections[index + 1] = st.session_state.sections[index + 1], st.session_state.sections[index]
    for i, section in enumerate(st.session_state.sections):
        section['order'] = i

def update_section(index, key, value):
    st.session_state.sections[index][key] = value

def generate_html():
    html = "<html><head><title>My Custom Page</title></head><body>"
    for section in sorted(st.session_state.sections, key=lambda x: x['order']):
        if section['type'] == 'text':
            html += f"<div style='padding: 20px;'>"
            html += f"<h2>{section['title']}</h2>"
            html += f"<p>{section['content']}</p>"
            html += "</div>"
        elif section['type'] == 'image' and section['image']:
            html += f"<div style='padding: 20px;'>"
            html += f"<h2>{section['title']}</h2>"
            html += f"<img src='{section['image']}' style='max-width: 100%;'>"
            html += "</div>"
    html += "</body></html>"
    return html

def save_template():
    template = {'sections': st.session_state.sections}
    return json.dumps(template)

def load_template(template_json):
    template = json.loads(template_json)
    st.session_state.sections = template['sections']

# アプリの名前と説明
st.title("My Custom Page Builder")
st.write("このアプリを使って、オリジナルのウェブページを簡単に作成できます。")

st.header("セクションの設定")

# セクション追加ボタン
st.subheader("セクションを追加")
if st.button("テキストセクションを追加"):
    add_section('text')
if st.button("画像セクションを追加"):
    add_section('image')

# セクションの表示
for index, section in enumerate(st.session_state.sections):
    st.subheader(f"セクション {index+1}")
    if section['type'] == 'text':
        title = st.text_input(f"セクション {index+1} のタイトル", section['title'], key=f"title_{index}")
        content = st.text_area(f"セクション {index+1} の内容", section['content'], key=f"content_{index}")
        update_section(index, 'title', title)
        update_section(index, 'content', content)
    elif section['type'] == 'image':
        title = st.text_input(f"セクション {index+1} のタイトル", section['title'], key=f"title_{index}")
        image = st.file_uploader(f"セクション {index+1} の画像", type=["jpg", "png", "jpeg"], key=f"image_{index}")
        if image:
            image_data = base64.b64encode(image.read()).decode()
            image_url = f"data:image/jpeg;base64,{image_data}"
            update_section(index, 'image', image_url)
        update_section(index, 'title', title)

    # セクションの順番変更
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(f"↑", key=f"up_{index}"):
            move_section(index, 'up')
    with col2:
        if st.button(f"↓", key=f"down_{index}"):
            move_section(index, 'down')
    with col3:
        if st.button(f"セクション {index+1} を削除", key=f"remove_{index}"):
            remove_section(index)

# ページ生成ボタン
if st.button("ページを生成"):
    st.markdown("### 生成されたページ")
    for section in sorted(st.session_state.sections, key=lambda x: x['order']):
        if section['type'] == 'text':
            st.markdown(f"""
            <div style="padding: 20px;">
                <h2>{section['title']}</h2>
                <p>{section['content']}</p>
            </div>
            """, unsafe_allow_html=True)
        elif section['type'] == 'image' and section['image']:
            st.markdown(f"""
            <div style="padding: 20px;">
                <h2>{section['title']}</h2>
                <img src="{section['image']}" style="max-width: 100%;">
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

# テンプレートの保存とロード
st.sidebar.title("テンプレートの保存とロード")
template_json = st.sidebar.text_area("テンプレート JSON", "")
if st.sidebar.button("テンプレートをロード"):
    load_template(template_json)
st.sidebar.download_button(
    label="テンプレートを保存",
    data=save_template(),
    file_name="template.json",
    mime="application/json"
)

# サイドバーでプレビュー表示
st.sidebar.title("ページのプレビュー")
for section in sorted(st.session_state.sections, key=lambda x: x['order']):
    if section['type'] == 'text':
        st.sidebar.markdown(f"""
        <div style="padding: 20px;">
            <h2>{section['title']}</h2>
            <p>{section['content']}</p>
        </div>
        """, unsafe_allow_html=True)
    elif section['type'] == 'image' and section['image']:
        st.sidebar.markdown(f"""
        <div style="padding: 20px;">
            <h2>{section['title']}</h2>
            <img src="{section['image']}" style="max-width: 100%;">
        </div>
        """, unsafe_allow_html=True)

