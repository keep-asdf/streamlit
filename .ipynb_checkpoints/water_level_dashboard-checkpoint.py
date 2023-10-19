import streamlit as st
import pandas as pd
from visualizations import visualize_last_6_hours_with_moving_averages_bokeh
from bokeh.plotting import figure

# 페이지 설정: 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="Water Level Predictions", layout="wide")

# 앱의 타이틀 설정
st.title("Water Level Predictions with Confidence Interval")

# 데이터 로드
@st.cache
def load_data():
    return pd.read_csv('data/pred_with_CI.csv')

data = load_data()

# Bokeh를 사용하여 그래프 그리기
fig = visualize_last_6_hours_with_moving_averages_bokeh(data)

# Bokeh 그래프를 Streamlit에 표시
st.bokeh_chart(fig)

# 어두운 테마 적용을 위한 CSS
st.markdown("""
<style>
body {
    color: #fff;
    background-color: #4F4F4F;
}
</style>
    """, unsafe_allow_html=True)
