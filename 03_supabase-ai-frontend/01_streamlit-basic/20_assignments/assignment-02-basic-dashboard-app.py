import streamlit as st


st.set_page_config(page_title="학습 대시보드", layout="wide")

st.title("나의 학습 대시보드")
st.write("사이드바에서 설정을 바꾸면 학습 현황이 함께 변경됩니다.")

# 사이드바는 사용자의 설정을 입력하는 영역입니다.
with st.sidebar:
    st.header("학습 설정")
    user_name = st.text_input("사용자 이름")
    study_level = st.selectbox("현재 학습 단계", ["입문", "중급", "고급"])
    study_hours = st.slider("이번 주 학습 시간", min_value=0, max_value=20, value=5)
    weekly_goal = st.slider("이번 주 목표 시간", min_value=1, max_value=20, value=10)

# 입력한 시간을 기준으로 진행률과 남은 시간을 계산합니다.
progress_rate = min(int(study_hours / weekly_goal * 100), 100)
remaining_hours = max(weekly_goal - study_hours, 0)

if not user_name:
    st.warning("사이드바에 사용자 이름을 입력해 주세요.")
else:
    st.success(f"{user_name}님의 {study_level} 학습 현황입니다.")

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("이번 주 학습 시간", f"{study_hours}시간")
metric_col2.metric("주간 목표", f"{weekly_goal}시간")
metric_col3.metric("목표 달성률", f"{progress_rate}%")

st.divider()

overview_tab, detail_tab = st.tabs(["개요", "상세 내용"])

with overview_tab:
    st.subheader("이번 주 진행 상황")
    st.progress(progress_rate)

    if study_hours >= weekly_goal:
        st.success("이번 주 학습 목표를 달성했습니다!")
    elif study_hours == 0:
        st.info("학습을 시작하면 진행률이 표시됩니다.")
    else:
        st.info(f"목표까지 {remaining_hours}시간 남았습니다.")

with detail_tab:
    st.subheader("학습 설정 요약")
    st.write(f"- 사용자 이름: {user_name or '입력 전'}")
    st.write(f"- 현재 학습 단계: {study_level}")
    st.write(f"- 이번 주 학습 시간: {study_hours}시간")
    st.write(f"- 이번 주 목표 시간: {weekly_goal}시간")
