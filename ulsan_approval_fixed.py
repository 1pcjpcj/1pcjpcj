# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
import io
import urllib.parse

# Optional: requests used only when fetching image from GitHub raw URL
try:
    import requests
except Exception:
    requests = None

st.set_page_config(page_title="결재 시스템 (울산)", layout="wide")

# --- IMAGE LOADER (local first, then GitHub raw URL) ---
IMAGE_NAME = "AI수도 울산 산업수도 울산(한줄).png"  # 사용하실 이미지 파일명
def load_image():
    # 1) local file in repo root
    if os.path.exists(IMAGE_NAME):
        return IMAGE_NAME
    # 2) try GitHub raw URL (URL-encode filename)
    raw_url = "https://raw.githubusercontent.com/1pcjpcj/1pcjpcj/main/" + urllib.parse.quote(IMAGE_NAME)
    if requests is not None:
        try:
            r = requests.get(raw_url, timeout=8)
            if r.status_code == 200:
                return io.BytesIO(r.content)
        except Exception as e:
            # ignore, will return None
            pass
    return None

img = load_image()
if img:
    # use_container_width is supported in recent Streamlit releases
    try:
        st.image(img, use_container_width=True)
    except TypeError:
        # fallback for older streamlit versions
        st.image(img)
else:
    st.warning("이미지를 불러오지 못했습니다. GitHub에 업로드된 이미지 이름과 위치를 확인하거나, repo 루트에 이미지 파일을 올려주세요.")
    st.caption(f"원하는 파일명: {IMAGE_NAME} (repo root 또는 main branch raw URL 사용)")

# --- initialize session data ---
if "documents" not in st.session_state:
    st.session_state.documents = pd.DataFrame(columns=["문서명", "상태"])

# sample data if empty (helpful for first run)
if st.session_state.documents.empty:
    st.session_state.documents = pd.DataFrame([
        ["기업지원과-보조금", "대기 중"],
        ["투자유치과-투자", "대기 중"],
        ["교통기획과-로터리", "대기 중"]
    ], columns=["문서명", "상태"])

# --- sidebar: new document registration (big input suggested) ---
st.sidebar.header("🆕 신규 결재 등록")
new_doc = st.sidebar.text_input("문서 제목 입력 (예: 부서-문서명)", max_chars=120)
if st.sidebar.button("등록하기"):
    title = new_doc.strip() if new_doc.strip() != "" else "제목 없음"
    st.session_state.documents.loc[len(st.session_state.documents)] = [title, "대기 중"]
    st.success(f"'{title}' 문서를 등록했습니다.")
    st.experimental_rerun()

# --- main header ---
st.markdown("<h1 style='font-size:28px;'>🏢 결재 진행 현황</h1>", unsafe_allow_html=True)

current = st.session_state.documents[st.session_state.documents["상태"] == "결재 중"]
waiting = st.session_state.documents[st.session_state.documents["상태"] == "대기 중"]

if not current.empty:
    st.markdown(f"<div style='font-size:20px;'>🟥 <strong>현재 결재 중:</strong> {current.iloc[0]['문서명']}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='font-size:20px;'>⌛ 현재 결재 중인 문서가 없습니다.</div>", unsafe_allow_html=True)

if not waiting.empty:
    st.markdown(f"<div style='font-size:18px; margin-top:8px;'>📄 다음 대기 문서: {waiting.iloc[0]['문서명']}</div>", unsafe_allow_html=True)
else:
    st.markdown("<div style='font-size:18px; margin-top:8px;'>📄 다음 대기 문서가 없습니다.</div>", unsafe_allow_html=True)

st.markdown("---")

# --- center big management area ---
st.markdown("<h2 style='text-align:center;'>👩‍💼 상신 문서 관리 (가운데, 확대 표시)</h2>", unsafe_allow_html=True)
left, center, right = st.columns([1, 3, 1])

with center:
    st.markdown("<div style='background:white;padding:18px;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,0.06);'>", unsafe_allow_html=True)
    # iterate using index to allow stable updates
    for idx in st.session_state.documents.index:
        row = st.session_state.documents.loc[idx]
        name = row["문서명"]
        status = row["상태"]
        st.markdown(f"<div style='display:flex;align-items:center;justify-content:space-between;padding:10px 6px;border-bottom:1px solid #f0f0f0;'>"
                    f"<div style='font-size:18px; font-weight:600;'>{idx+1}. {name}</div>"
                    f"<div style='font-size:14px;color:#666;margin-left:12px;'>{status}</div>"
                    f"</div>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,1,1])

        # 결재 시작: if already '결재 중' show red non-clickable badge; otherwise show button
        if status == "결재 중":
            # show red badge instead of clickable start button
            c1.markdown("<div style='background:#ff4d4d;color:white;padding:6px 10px;border-radius:8px;text-align:center;font-weight:700;'>결재 중</div>", unsafe_allow_html=True)
        else:
            if c1.button("결재 시작", key=f"start_{idx}"):
                # set all to '대기 중' first (only one active at a time)
                st.session_state.documents.loc[:, "상태"] = st.session_state.documents.loc[:, "상태"].replace("결재 중", "대기 중")
                st.session_state.documents.loc[idx, "상태"] = "결재 중"
                st.experimental_rerun()

        if c2.button("완료", key=f"done_{idx}"):
            st.session_state.documents.loc[idx, "상태"] = "완료"
            st.experimental_rerun()

        if c3.button("삭제", key=f"del_{idx}"):
            st.session_state.documents = st.session_state.documents.drop(idx).reset_index(drop=True)
            st.experimental_rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --- footer tips ---
st.markdown("---")
st.caption("Tip: 앱을 TV에서 전체화면(F11)으로 띄우면 관리화면이 더 잘 보입니다.")

