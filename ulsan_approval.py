
import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="결재 진행 현황", layout="wide")

# 상단에 로고 또는 이미지 추가 (AI 수도 울산 이미지)
st.image("https://raw.githubusercontent.com/1pcjpcj/1pcjpcj/main/AI%EC%88%98%EB%8F%84%20%EC%9A%B8%EC%82%B0%20%EC%82%B0%EC%97%85%EC%88%98%EB%8F%84%20%EC%9A%B8%EC%82%B0(%ED%95%9C%EC%A4%84).png", use_column_width=True)

# 데이터 초기화
if "documents" not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=["이름", "상태"])

# 사이드바 (결재 등록)
st.sidebar.header("📝 신규 결재 등록")
new_doc = st.sidebar.text_input("결재 제목 또는 이름 입력")
if st.sidebar.button("등록하기") and new_doc:
    new_row = pd.DataFrame([[new_doc, "대기 중"]], columns=["이름", "상태"])
    st.session_state.documents = pd.concat([st.session_state.documents, new_row], ignore_index=True)
    st.rerun()

# 상태 업데이트 함수
def update_status(index, new_status):
    st.session_state.documents.at[index, "상태"] = new_status
    st.rerun()

# 두 영역 나누기 (왼쪽: 결재 현황 / 오른쪽: 관리자용 제어)
col1, col2 = st.columns([2.5, 1])

# 왼쪽: 결재 진행 현황
with col1:
    st.markdown("## 🏢 결재 진행 현황")

    current = st.session_state.documents[st.session_state.documents["상태"] == "결재 중"]
    waiting = st.session_state.documents[st.session_state.documents["상태"] == "대기 중"]

    if not current.empty:
        st.markdown(f"### 🟢 현재 결재 중: **{current.iloc[0]['이름']} 문서**")
    else:
        st.markdown("### ⏳ 현재 결재 중인 문서가 없습니다.")

    if not waiting.empty:
        st.markdown(f"#### 다음 대기 문서: {waiting.iloc[0]['이름']}")
    else:
        st.markdown("#### 다음 대기 문서가 없습니다.")

# 오른쪽: 관리자용 제어
with col2:
    st.markdown("## 👩‍💼 상신 문서 관리")
    for i, row in st.session_state.documents.iterrows():
        name, status = row["이름"], row["상태"]
        st.write(f"**{i+1}. {name}** — {status}")
        cols = st.columns(3)
        if cols[0].button("결재 시작", key=f"start_{i}"):
            update_status(i, "결재 중")
        if cols[1].button("완료", key=f"done_{i}"):
            update_status(i, "완료")
        if cols[2].button("삭제", key=f"del_{i}"):
            st.session_state.documents = st.session_state.documents.drop(i).reset_index(drop=True)
            st.rerun()
