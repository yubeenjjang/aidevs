import streamlit as st


st.title("자기소개 앱")
st.info("이름, 관심 분야, 자기소개를 모두 입력해 주세요.")

# 사용자에게 자기소개에 필요한 세 가지 정보를 입력받습니다.
name = st.text_input("이름을 입력하세요")
interest = st.selectbox(
    "관심 있는 분야를 선택하세요",
    ["선택하세요", "백엔드", "프론트엔드"],
)
introduction = st.text_area("자기소개를 입력하세요")

st.divider()

# 모든 입력값이 있을 때만 자기소개 카드를 출력합니다.
if name and interest != "선택하세요" and introduction:
    st.success("자기소개 카드가 완성되었습니다.")

    with st.container(border=True):
        st.subheader(f"{name}님의 자기소개")
        st.write(f"관심 분야: {interest}")
        st.write(f"자기소개: {introduction}")
else:
    # 아직 입력하지 않은 항목만 모아서 안내합니다.
    missing_fields = []
    if not name:
        missing_fields.append("이름")
    if interest == "선택하세요":
        missing_fields.append("관심 분야")
    if not introduction:
        missing_fields.append("자기소개")

    st.warning(f"다음 항목을 입력해 주세요: {', '.join(missing_fields)}")
