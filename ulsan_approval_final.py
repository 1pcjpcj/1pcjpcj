
import streamlit as st
import pandas as pd
import base64

# 페이지 설정
st.set_page_config(page_title="울산 결재 시스템", layout="wide")

# 로고 이미지 표시
st.image("AI수도 울산 산업수도 울산(한줄).png", use_container_width=True)

st.title("🏢 결재 진행 현황")

# 초기 데이터
if "docs" not in st.session_state:
    st.session_state.docs = pd.DataFrame(columns=["문서명", "상태"])

# 신규 문서 등록
with st.sidebar:
    st.header("🆕 신규 결재 등록")
    new_doc = st.text_input("문서 제목 입력 (예: 투자유치과-투자)")
    if st.button("등록하기"):
        if new_doc.strip() != "":
            new_row = pd.DataFrame([[new_doc, "대기 중"]], columns=["문서명", "상태"])
            st.session_state.docs = pd.concat([st.session_state.docs, new_row], ignore_index=True)
            st.success(f"{new_doc} 문서가 등록되었습니다.")
            st.rerun()

# 현재 결재 중/대기 중 표시
current = st.session_state.docs[st.session_state.docs["상태"] == "결재 중"]
waiting = st.session_state.docs[st.session_state.docs["상태"] == "대기 중"]

if not current.empty:
    st.markdown(f"### ⏳ 현재 결재 중: **{current.iloc[0]['문서명']}**")
else:
    st.markdown("### ⏳ 현재 결재 중인 문서가 없습니다.")

if not waiting.empty:
    st.markdown(f"📄 다음 대기 문서: {waiting.iloc[0]['문서명']}")
else:
    st.markdown("📄 다음 대기 문서가 없습니다.")

# 상신 문서 관리 (가운데 정렬, 확대)
st.markdown("---")
st.markdown("<h2 style='text-align:center;'>👩‍💼 상신 문서 관리 (가운데, 확대 표시)</h2>", unsafe_allow_html=True)

col_center = st.columns([0.2, 0.6, 0.2])[1]

with col_center:
    for i, row in st.session_state.docs.iterrows():
        name, status = row["문서명"], row["상태"]
        st.write(f"**{i+1}. {name}** — {status}")

        cols = st.columns(3)
        start_btn = cols[0].button("결재 시작", key=f"start_{i}")
        done_btn = cols[1].button("완료", key=f"done_{i}")
        del_btn = cols[2].button("삭제", key=f"del_{i}")

        if start_btn:
            st.session_state.docs.at[i, "상태"] = "결재 중"
            st.rerun()

        if done_btn:
            st.session_state.docs.at[i, "상태"] = "완료"
            # 결재 완료시 알림음 재생
            audio_file = open("success.mp3", "rb")
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
            st.success(f"{name} 문서 결재가 완료되었습니다!")
            st.rerun()

        if del_btn:
            st.session_state.docs = st.session_state.docs.drop(i).reset_index(drop=True)
            st.rerun()
