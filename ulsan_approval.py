import streamlit as st
import pandas as pd

# --- 기본 설정 ---
st.set_page_config(page_title="결재 시스템", layout="wide")

# --- AI 수도 울산 이미지 삽입 ---
st.image("AI수도 울산 산업수도 울산(한줄).png", use_container_width=True)

# --- 세션 상태 초기화 ---
if "documents" not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=["문서명", "상태"])

# --- 새 결재 문서 등록 ---
st.sidebar.header("🆕 신규 결재 등록")
new_doc = st.sidebar.text_input("문서 제목 입력")
if st.sidebar.button("등록하기"):
    if new_doc:
        st.session_state.documents.loc[len(st.session_state.documents)] = [new_doc, "대기 중"]
        st.rerun()

# --- 결재 진행 현황 ---
st.header("🏢 결재 진행 현황")

current = st.session_state.documents[st.session_state.documents["상태"] == "결재 중"]
waiting = st.session_state.documents[st.session_state.documents["상태"] == "대기 중"]

if not current.empty:
    st.markdown(f"🟥 **현재 결재 중:** {current.iloc[0]['문서명']} 문서")
else:
    st.markdown("⌛ 현재 결재 중인 문서가 없습니다.")

if not waiting.empty:
    st.markdown(f"📄 다음 대기 문서: {waiting.iloc[0]['문서명']}")
else:
    st.markdown("✅ 모든 문서 결재 완료!")

# --- 상신 문서 관리 (중앙 정렬 및 확대) ---
st.markdown("<h2 style='text-align:center;'>👩‍💼 상신 문서 관리</h2>", unsafe_allow_html=True)

center = st.container()
with center:
    cols = st.columns([1, 2, 2, 2, 1])  # 가운데 정렬
    with cols[2]:
        for i, row in st.session_state.documents.iterrows():
            st.markdown(f"### {i+1}. {row['문서명']} — {row['상태']}")
            c1, c2, c3 = st.columns([1, 1, 1])

            # 결재 시작 버튼 (빨간색 활성화)
            if row["상태"] == "결재 중":
                button_style = "background-color:red; color:white; font-weight:bold;"
            else:
                button_style = "background-color:#E0E0E0; color:black;"

            button_html = f"""
            <form action="" method="get">
                <button style="{button_style}" type="submit">결재 시작</button>
            </form>
            """
            c1.markdown(button_html, unsafe_allow_html=True)

            # 완료 버튼
            if c2.button("완료", key=f"done_{i}"):
                st.session_state.documents.loc[i, "상태"] = "완료"
                st.rerun()

            # 삭제 버튼
            if c3.button("삭제", key=f"del_{i}"):
                st.session_state.documents = st.session_state.documents.drop(i).reset_index(drop=True)
                st.rerun()

# --- 하단 안내 ---
st.markdown("---")
st.caption("울산광역시 AI 수도·산업수도 울산 결재 시스템 © 2025")
