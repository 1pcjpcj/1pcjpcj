import streamlit as st
from PIL import Image

# 페이지 설정
st.set_page_config(page_title="울산 결재 시스템", layout="wide")

# AI 수도 울산 이미지 로드
st.image("AI수도 울산 산업수도 울산(한줄).png", use_container_width=True)

st.markdown("## 🏢 결재 진행 현황")

# 세션 상태 초기화
if "documents" not in st.session_state:
    st.session_state.documents = [
        {"title": "기업지원과-보조금", "status": "대기 중"},
        {"title": "투자유치과-투자", "status": "대기 중"},
        {"title": "교통기획과-로터리", "status": "대기 중"}
    ]
if "current" not in st.session_state:
    st.session_state.current = None

# 현재 결재 진행 중 문서
current_doc = next((doc for doc in st.session_state.documents if doc["status"] == "진행 중"), None)
if current_doc:
    st.markdown(f"⏳ **현재 결재 중:** {current_doc['title']} ")
else:
    st.markdown("⏳ **현재 결재 중인 문서가 없습니다.**")

# 다음 대기 문서 표시
waiting_docs = [d for d in st.session_state.documents if d["status"] == "대기 중"]
if waiting_docs:
    st.markdown(f"📄 다음 대기 문서: {waiting_docs[0]['title']}")
else:
    st.markdown("✅ 모든 문서 결재 완료!")

st.markdown("---")

# 중앙 정렬 + 확대
st.markdown("<h3 style='text-align:center;'>👩‍💼 상신 문서 관리 (가운데, 확대 표시)</h3>", unsafe_allow_html=True)
st.markdown("<div style='display:flex; justify-content:center;'>", unsafe_allow_html=True)

# 각 문서 카드 표시
for i, doc in enumerate(st.session_state.documents, 1):
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    with col1:
        st.markdown(f"**{i}. {doc['title']}** — {doc['status']}")
    with col2:
        if st.button("결재 시작", key=f"start_{i}"):
            for d in st.session_state.documents:
                d["status"] = "대기 중"
            doc["status"] = "진행 중"
            st.rerun()
        if doc["status"] == "진행 중":
            st.markdown("<span style='color:red; font-weight:bold;'>결재 진행 중 🔥</span>", unsafe_allow_html=True)
    with col3:
        if st.button("완료", key=f"done_{i}"):
            doc["status"] = "완료"
            st.rerun()
    with col4:
        if st.button("삭제", key=f"delete_{i}"):
            st.session_state.documents.remove(doc)
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# 왼쪽 사이드바
st.sidebar.header("🆕 신규 결재 등록")
new_title = st.sidebar.text_input("문서 제목 입력 (예: 부서-문서명)")
if st.sidebar.button("등록하기"):
    if new_title:
        st.session_state.documents.append({"title": new_title, "status": "대기 중"})
        st.sidebar.success("✅ 문서가 등록되었습니다!")
        st.rerun()
    else:
        st.sidebar.warning("⚠ 문서 제목을 입력해주세요.")
