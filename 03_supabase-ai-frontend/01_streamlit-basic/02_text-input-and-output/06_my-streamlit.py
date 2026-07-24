from pathlib import Path

import streamlit as st


st.title("my-streamlit")

current_file = Path(__file__).resolve()
image_path = current_file.parent.parent / "imgs" / "image.png"

st.image(
    image_path,
    use_container_width=True,
)

snorlax_age = st.number_input(
    "나이",
    min_value=0,
    max_value=120,
    value=20,
)
st.write(f"이 포켓몬의 나이는 {snorlax_age}살입니다.")

entered_name = st.text_input("포켓몬 이름을 입력하세요")

if entered_name:
    if entered_name == "잠만보":
        st.info("잠만보는 하루 대부분을 잠을 자며 보냅니다.")
    else:
        st.info("땡")

selected_character = st.selectbox(
    "포켓몬 이름을 선택하세요",
    ["선택하세요", "피카츄", "잠만보", "꼬부기"],
)

if selected_character != "선택하세요":
    if selected_character == "잠만보":
        st.info("잠만보는 하루 대부분을 잠을 자며 보냅니다.")
    else:
        st.info("땡")
