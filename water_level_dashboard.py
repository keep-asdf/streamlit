import streamlit as st
import pandas as pd
from visualizations import visualize_moving_averages_with_cross_highlighted

# 데이터를 로드합니다.
@st.cache
def load_data():
    return pd.read_csv('data/water_level_with_moving_averages.csv')  # 실제 데이터 경로로 바꾸세요.

data = load_data()

st.title("Water Level Dashboard")

# 데이터 프레임을 그래프로 표시합니다.
st.write("Predicted MHC Water Level Visualization")

# 데이터의 복사본을 사용하여 시각화 함수를 호출합니다.
visualize_moving_averages_with_cross_highlighted(data.copy())

st.write(data)  # 데이터 프레임을 표로도 표시합니다.
