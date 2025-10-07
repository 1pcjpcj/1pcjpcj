
import streamlit as st

st.set_page_config(page_title="AI 수도 울산 산업수도 울산", layout="wide")

page_bg = """
<style>
body {
    background-color: #fff;
    font-family: 'NanumSquare', sans-serif;
    text-align: center;
}
h1 {
    background: linear-gradient(90deg, #A000D6, #E2004C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 64px;
    font-weight: 900;
    margin-top: 100px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.1);
}
h3 {
    color: #444;
    font-size: 22px;
    margin-top: -10px;
}
button, .stButton>button {
    background: linear-gradient(90deg, #E2004C, #A000D6);
    color: white;
    font-size: 20px;
    border: none;
    border-radius: 12px;
    padding: 10px 30px;
    transition: all 0.3s ease;
}
button:hover, .stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #A000D6, #E2004C);
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.markdown("<h1>AI 수도 울산<br>산업수도 울산</h1>", unsafe_allow_html=True)
st.markdown("<h3>미래를 준비하는 도시, 울산이 앞장섭니다.</h3>", unsafe_allow_html=True)

if st.button("울산 미래 비전 보기"):
    st.success("🚀 울산은 AI와 산업이 공존하는 미래형 도시로 도약 중입니다!")
