import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정: 페이지 제목 및 레이아웃 설정
st.set_page_config(page_title="Water Level Predictions", layout="wide")

# 앱의 타이틀 설정
st.title("Water Level Predictions with Confidence Interval")

# 데이터 로드
@st.cache
def load_data():
    return pd.read_csv('predicted_values_with_CI.csv')

data = load_data()

# Plotly를 사용하여 그래프 그리기
fig = px.line(data, x='Time', y='Predicted_MHC_Water_Level', title='Predicted MHC Water Level')
fig.add_scatter(x=data['Time'], y=data['CI_Lower'], mode='lines', name='CI Lower')
fig.add_scatter(x=data['Time'], y=data['CI_Upper'], mode='lines', name='CI Upper')

st.plotly_chart(fig)

# 어두운 테마 적용을 위한 CSS
st.markdown("""
<style>
body {
    color: #fff;
    background-color: #4F4F4F;
}
</style>
    """, unsafe_allow_html=True)
