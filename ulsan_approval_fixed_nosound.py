
import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI 수도 울산 결재 시스템", layout="wide")

# 헤더 이미지
st.image("AI수도 울산 산업수도 울산(한줄).png", use_container_width=True)

if "docs" not in st.session_state:
    st.session_state.docs = pd.DataFrame(columns=["문서명", "상태"])

# 신규 결재 등록
st.sidebar.header("🆕 신규 결재 등록")
new_doc = st.sidebar.text_input("문서 제목 입력 (예: 부서-문서명)")
if st.sidebar.button("등록하기") and new_doc:
    new_row = pd.DataFrame([[new_doc, "대기 중"]], columns=["문서명", "상태"])
    st.session_state.docs = pd.concat([st.session_state.docs, new_row], ignore_index=True)
    st.rerun()

# 현재 결재 상태
st.markdown("## 🏢 결재 진행 현황")
current = st.session_state.docs[st.session_state.docs["상태"] == "결재 중"]
waiting = st.session_state.docs[st.session_state.docs["상태"] == "대기 중"]

if not current.empty:
    st.markdown(f"⏳ 현재 결재 중: **{current.iloc[0]['문서명']}**")
else:
    st.markdown("✅ 현재 결재 중인 문서가 없습니다.")

if not waiting.empty:
    st.markdown(f"📄 다음 대기 문서: {waiting.iloc[0]['문서명']}")

st.divider()

# 상신 문서 관리
st.markdown("### 🙋‍♀️ 상신 문서 관리 (가운데, 확대 표시)")
center = st.columns([1, 3, 1])[1]

with center:
    for i, row in st.session_state.docs.iterrows():
        name, status = row["문서명"], row["상태"]
        cols = st.columns([2, 1, 1, 1])
        with cols[0]:
            st.markdown(f"**{i+1}. {name}** — {status}")
        with cols[1]:
            if st.button("결재 시작", key=f"start_{i}"):
                st.session_state.docs.at[i, "상태"] = "결재 중"
                st.rerun()
        with cols[2]:
            if st.button("완료", key=f"done_{i}"):
                st.session_state.docs.at[i, "상태"] = "완료"
                st.rerun()
        with cols[3]:
            if st.button("삭제", key=f"del_{i}"):
                st.session_state.docs = st.session_state.docs.drop(i).reset_index(drop=True)
                st.rerun()
