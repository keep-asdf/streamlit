import pandas as pd
import plotly.express as px
import streamlit as st

    
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
    
    
if __name__ == "__main__":
    main()
