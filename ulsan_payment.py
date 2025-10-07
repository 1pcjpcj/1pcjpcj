
import streamlit as st
import pandas as pd
import datetime

# ---------- 설정 ----------
st.set_page_config(page_title="울산 결제 안내 (AI 수도 울산)", layout="wide")

# 이미지: (GitHub에 업로드한 이미지 경로를 사용합니다)
# 파일명을 바꾸셨다면 아래 URL을 그 이름으로 바꿔주세요.
image_url = "https://raw.githubusercontent.com/1pcjpcj/1pcjpcj/main/AI%EC%88%98%EB%8F%84%20%EC%9A%B8%EC%82%B0%20%EC%82%B0%EC%97%85%EC%88%98%EB%8F%84%20%EC%9A%B8%EC%82%B0(%ED%95%9C%EC%A4%84).png"

# ---------- CSS 스타일 (큰 입력창 / 버튼 / 카드 등) ----------
st.markdown(
    """
    <style>
    /* 전체 배경과 폰트 */
    .main {background-color: #fff;}
    .title-gradient {
        background: linear-gradient(90deg,#A000D6,#E2004C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 48px;
        margin-bottom: 6px;
    }
    .subtitle { color: #444; font-size:18px; margin-top: -8px; margin-bottom: 18px; }

    /* 큰 입력창 (모바일/태블릿/TV 모두 가독성 좋게) */
    input[type="text"], input[type="number"] {
        font-size: 28px !important;
        padding: 12px !important;
        height:48px !important;
    }
    textarea {
        font-size: 24px !important;
    }
    .stButton>button, button {
        font-size: 20px !important;
        padding: 12px 24px !important;
        border-radius: 10px !important;
        background: linear-gradient(90deg,#E2004C,#A000D6) !important;
        color: white !important;
        border: none !important;
    }

    /* 안내 박스 */
    .status-box {
        background: white;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.08);
        text-align: left;
    }
    .status-current { font-size: 34px; font-weight:700; color:#b30059; }
    .status-next { font-size: 22px; color:#333; margin-top:8px; }

    /* 직원 리스트 */
    .staff-row { padding:10px 6px; border-bottom:1px solid #eee; display:flex; align-items:center; justify-content:space-between; }
    .staff-name { font-size:18px; }
    .staff-status { font-size:16px; color:#666; margin-right:8px; }

    /* 반응형 여백 */
    .top-padding { padding-top: 20px; }
    </style>
    """, unsafe_allow_html=True
)

# ---------- 로고 / 제목 ----------
col_logo = st.columns([1, 4, 1])
with col_logo[1]:
    try:
        st.image(image_url, use_column_width=True)
    except Exception:
        st.markdown("<div style='text-align:center'><h2 class='title-gradient'>AI 수도 울산<br>산업수도 울산</h2></div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>미래를 준비하는 도시, 울산이 앞장섭니다.</div>", unsafe_allow_html=True)

# ---------- 세션 데이터 초기화 ----------
if "customers" not in st.session_state:
    st.session_state.customers = pd.DataFrame(columns=["이름", "상태", "등록시간"])

# 기본 테스트 데이터 (없을 때만 넣음)
if st.session_state.customers.empty:
    st.session_state.customers = pd.DataFrame([
        ["박지훈", "결제 중", datetime.datetime.now().strftime("%H:%M:%S")],
        ["김민수", "대기 중", datetime.datetime.now().strftime("%H:%M:%S")]
    ], columns=["이름","상태","등록시간"])

# ---------- 레이아웃: 좌(큰 등록+안내) / 우(직원 관리) ----------
col_left, col_right = st.columns([2.5, 1])

# ----- 왼쪽: 큰 결제 등록/안내 화면 -----
with col_left:
    st.markdown("<div class='top-padding'></div>", unsafe_allow_html=True)
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)

    # 큰 등록 UI
    st.markdown("<h3 style='margin-bottom:6px'>🧾 결제 등록 (크게 보이는 입력창)</h3>", unsafe_allow_html=True)
    st.markdown("<div style='margin-bottom:6px;color:#666'>고객 이름을 입력하고 '대기 등록' 버튼을 눌러주세요.</div>", unsafe_allow_html=True)

    name_input = st.text_input("고객 이름", key="reg_name", placeholder="예: 홍길동")
    amount_input = st.text_input("결제 금액 (선택)", key="reg_amount", placeholder="예: 35,000원 (선택)")

    register_cols = st.columns([1,1,1])
    if register_cols[0].button("대기 등록", key="btn_register"):
        new_row = {"이름": name_input.strip() if name_input.strip() != "" else "이름없음", 
                   "상태": "대기 중", 
                   "등록시간": datetime.datetime.now().strftime("%H:%M:%S")}
        st.session_state.customers = pd.concat([st.session_state.customers, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"{new_row['이름']}님이 대기 등록되었습니다.")
        st.experimental_rerun()

    if register_cols[1].button("즉시 결제 시작 (다음)", key="btn_start_next"):
        # 결제 중이 없으면 가장 첫 대기자를 결제중으로 변경
        waiting = st.session_state.customers[st.session_state.customers["상태"]=="대기 중"]
        if not waiting.empty:
            idx = waiting.index[0]
            st.session_state.customers.at[idx,"상태"] = "결제 중"
            st.experimental_rerun()
        else:
            st.info("대기 중인 고객이 없습니다.")

    register_cols[2].button("폼 초기화", key="btn_reset_form")  # 단순 리셋 (입력상자 내용은 수동으로 지우기)

    st.markdown("<hr>", unsafe_allow_html=True)

    # 결제 안내 표시 (크게)
    current = st.session_state.customers[st.session_state.customers["상태"] == "결제 중"]
    waiting = st.session_state.customers[st.session_state.customers["상태"] == "대기 중"]

    if not current.empty:
        cur_name = current.iloc[0]["이름"]
        st.markdown(f"<div class='status-current'>🟢 현재 결제 중: {cur_name} 고객님</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='status-current'>⏳ 현재 결제 중인 고객이 없습니다.</div>", unsafe_allow_html=True)

    if not waiting.empty:
        st.markdown(f"<div class='status-next'>다음 대기: {waiting.iloc[0]['이름']} 고객님</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='status-next'>다음 대기 고객이 없습니다.</div>", unsafe_allow_html=True)

    st.markdown("<br><div style='color:#666'>전체 대기열 (최근 등록 순)</div>", unsafe_allow_html=True)
    # 전체 대기 리스트 (표 형식)
    display_df = st.session_state.customers.copy()
    display_df.index = display_df.index + 1
    st.table(display_df[["이름","상태","등록시간"]])

    st.markdown("</div>", unsafe_allow_html=True)

# ----- 오른쪽: 직원용 관리 -----
with col_right:
    st.markdown("<div class='top-padding'></div>", unsafe_allow_html=True)
    st.markdown("<div class='status-box'>", unsafe_allow_html=True)
    st.markdown("<h3>🧑‍💼 직원용 관리</h3>", unsafe_allow_html=True)

    # 직원이 각 고객을 조작할 수 있는 리스트
    for i, row in st.session_state.customers.reset_index().iterrows():
        idx = int(row['index'])
        name = row['이름']
        status = row['상태']
        cols = st.columns([2,1,1])
        cols[0].markdown(f"**{idx+1}. {name}**  <div style='color:#666'>{status}</div>", unsafe_allow_html=True)
        if cols[1].button("결제시작", key=f"start_{idx}") and status != "결제 중":
            st.session_state.customers.at[idx,"상태"] = "결제 중"
            st.experimental_rerun()
        if cols[2].button("완료", key=f"done_{idx}") and status != "완료":
            st.session_state.customers.at[idx,"상태"] = "완료"
            st.experimental_rerun()
        # 삭제 버튼 (아래에 배치)
    st.markdown("<hr>", unsafe_allow_html=True)
    del_name = st.selectbox("삭제할 고객 선택", options=list(st.session_state.customers["이름"]), index=0 if len(st.session_state.customers)>0 else -1)
    if st.button("삭제 선택 고객", key="btn_del"):
        # 삭제 (첫 일치 항목 제거)
        df = st.session_state.customers
        idxs = df.index[df["이름"]==del_name].tolist()
        if idxs:
            st.session_state.customers = df.drop(idxs[0]).reset_index(drop=True)
            st.success(f"{del_name} 고객을 삭제했습니다.")
            st.experimental_rerun()
        else:
            st.error("고객을 찾을 수 없습니다.")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- 사용 팁 ----------
st.markdown("<div style='margin-top:18px;color:#888;font-size:13px'>Tip: TV나 모니터에서 전체화면(F11)로 열어 안내화면을 크게 표시하세요.</div>", unsafe_allow_html=True)
