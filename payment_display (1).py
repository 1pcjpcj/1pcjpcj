import streamlit as st
import pandas as pd

st.set_page_config(page_title="결제 안내", layout="wide")

# 데이터 초기화
if "customers" not in st.session_state:
    st.session_state.customers = pd.DataFrame(columns=["이름", "상태"])

# 사이드바 (등록)
st.sidebar.header("💁 새 고객 등록")
new_name = st.sidebar.text_input("이름 입력")
if st.sidebar.button("등록하기") and new_name:
    new_row = pd.DataFrame([[new_name, "대기 중"]], columns=["이름", "상태"])
    st.session_state.customers = pd.concat([st.session_state.customers, new_row], ignore_index=True)
    st.rerun()

# 상태 업데이트 함수
def update_status(index, new_status):
    st.session_state.customers.at[index, "상태"] = new_status
    st.rerun()

col1, col2 = st.columns([2, 1])

# 왼쪽: 안내 화면
with col1:
    st.markdown("## 💳 결제 안내 화면")

    current = st.session_state.customers[st.session_state.customers["상태"] == "결제 중"]
    waiting = st.session_state.customers[st.session_state.customers["상태"] == "대기 중"]

    if not current.empty:
        st.markdown(f"### 🟢 현재 결제 중: **{current.iloc[0]['이름']} 고객님**")
    else:
        st.markdown("### ⏳ 현재 결제 중인 고객이 없습니다.")

    if not waiting.empty:
        st.markdown(f"#### 다음 대기: {waiting.iloc[0]['이름']} 고객님")
    else:
        st.markdown("#### 다음 대기 고객이 없습니다.")

# 오른쪽: 직원 관리
with col2:
    st.markdown("## 🧑‍💼 직원용 관리")
    for i, row in st.session_state.customers.iterrows():
        name, status = row["이름"], row["상태"]
        st.write(f"**{i+1}. {name}** — {status}")
        cols = st.columns(3)
        if cols[0].button("결제시작", key=f"start_{i}"):
            update_status(i, "결제 중")
        if cols[1].button("완료", key=f"done_{i}"):
            update_status(i, "완료")
        if cols[2].button("삭제", key=f"del_{i}"):
            st.session_state.customers = st.session_state.customers.drop(i).reset_index(drop=True)
            st.rerun()
