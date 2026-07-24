# 01_login.py
import streamlit as st
from streamlit_local_storage import LocalStorage

# 선언 --------------------------
# loginout = st.query_params.get("loginout","logout")

storage = LocalStorage()
loginout = storage.getItem("loginout")

if "input_login_id" not in st.session_state:
    st.session_state.input_login_id = ""

if "input_login_pwd" not in st.session_state:
    st.session_state.input_login_pwd = ""

def reset():
    st.session_state.input_login_id = ""
    st.session_state.input_login_pwd = ""


# 화면 --------------------------
if loginout == "logout"  or loginout is None:
    st.title("LOGIN")
    with st.form("login_form"):
        input_id = st.text_input("ID 입력", key="input_login_id")
        input_pwd = st.text_input("PWD 입력",type="password", key="input_login_pwd")
        left, submit_area , reset_area, right = st.columns([1, 2, 2, 1])
        with submit_area:
            login_submit = st.form_submit_button("LOGIN", type="primary",use_container_width=True)
        with reset_area:
            reset = st.form_submit_button("RESET", on_click=reset, type="primary",use_container_width=True)
            
        if login_submit:
            if input_id == "id01" and input_pwd == "pwd01":
               storage.setItem("loginout","login")
            #    st.rerun()
            else:
                st.info("로그인 실패")
                
else:
    with st.sidebar:
        st.info("로그인 성공!")
    st.header("설문 조사")
    name = st.text_input("이름을 입력하세요")
    
    age = st.number_input("나이를 입력하세요", min_value=20, max_value=100, value=20) 
    
    interest = st.selectbox("관심 있는 분야를 선택하세요", ["백엔드", "프론트엔드", "AI"]) 
    
    languages = st.multiselect(
    "배운 프로그래밍 언어를 모두 선택하세요.",
    ["Python", "Java", "C", "SQL"]
    )
    
    hobby = st.text_area("취미를 작성해주세요","없음")
    
    major = st.checkbox("전공자입니다")
    if major:
        st.write("전공자")
    else:
        st.write("비전공자")
        
    satisfaction = st.slider("강의 만족도",min_value=1,max_value=5,value=3)
    
    
    with st.container(border = True):
        if st.button("설문 결과", type="primary") :
            if name:
                st.write(f"이름 : {name}")
            else:  
                st.info("이름을 입력해주세요")
                
            st.write(f"나이 : {age}")
            st.write(f"관심 분야 : {interest}")
            if languages:
                st.write(f"배운 프로그래밍 언어 : {languages}")
            else:
                st.write("배운 프로그래밍 언어 : 없음")
                
            st.write(f"취미 : {hobby}")
            if major:
                    st.write(f"전공 : 전공자")
            else:
                    st.write(f"전공 : 비전공자")
                    
            st.write(f"강의 만족도 : {satisfaction}")
            
    
    logout = st.button("LOGOUT", type="primary")
    if logout:
        storage.setItem("loginout","logout")
        # st.rerun()
    



