import streamlit as st
from visualizations import *
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu



st.set_page_config(layout="wide")

# Streamlit app
def main():
    st.title("미호천교 3시간 후 수위 예측 Dashboard")

    # 사이드바에 버튼을 추가합니다.
    update_button = st.sidebar.button("Update Data")
    
    
    # 사이드바를 사용하여 그래프 선택
    # graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

    
    # 사이드바를 사용하여 그래프 선택
    with st.sidebar:
        choice = option_menu("Menu", ["Prediction Result", "Learning Result"])
    

    
    if choice == "Prediction Result":
        # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
        
        with st.container():
            
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_data_moving_averages():
                return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

            data_moving_averages = load_data_moving_averages()

            # Convert the 'Time' column to datetime format
            data_moving_averages['Time'] = pd.to_datetime(data_moving_averages['Time'])

            # Check the last 6 hours of data
            last_6h_data = data_moving_averages.loc[data_moving_averages['Time'] >= data_moving_averages['Time'].iloc[-1] - pd.Timedelta(hours=6)]

            st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages))
             # 데이터 프레임과 그래프를 나란히 표시
            col1, col2 = st.columns(2)
            with col1:
                st.write(data_moving_averages.sort_values(by='Time', ascending=False))
            with col2:
                st.bokeh_chart(visualize_last_6h_moving_averages(last_6h_data))

            
            @st.cache_data(ttl=3600)  # 3600 sㅊeconds = 1 hour
            def load_water_data():
                return pd.read_csv('data/water_data.csv').copy()
       
            data_water_data = load_water_data().copy()
            # 각 feature에 대한 그래프 생성
            graphs = create_individual_graphs(data_water_data)
        
            # 2x3 그리드로 그래프 표시
            grid = gridplot([graphs[:3], graphs[3:]])
            st.bokeh_chart(grid)       
        
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def traffic_data():
                return pd.read_csv('data/traffic_data.csv').copy()

            traffic_data = traffic_data()
            st.subheader("실시간 미호천교 근방 교통 이벤트 데이터(empty = 현재 이벤트 없음)")
            st.write(traffic_data)
    
    elif choice == "Learning Result":
        
        placeholder = st.empty()
        with placeholder.container():
            
            # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_data_true_pred():
                return pd.read_csv('data/true_pred_with_CI.csv').copy()

            data_true_pred = load_data_true_pred()

            st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred))

            
            data_true_pred = load_data_true_pred()

            data_true_pred['Time'] = pd.to_datetime(data_true_pred['Time'])

            # Check the last 6 hours of data
            true_pred_last_6h_data = data_true_pred.loc[data_true_pred['Time'] >= data_true_pred['Time'].iloc[-1] - pd.Timedelta(hours=6)]

             # 데이터 프레임과 그래프를 나란히 표시
            col1, col2 = st.columns(2)
            with col1:
                st.write(data_true_pred.sort_values(by='Time', ascending=False))
            with col2:
                st.bokeh_chart(visualize_true_vs_predicted_last_6h(true_pred_last_6h_data))

if __name__ == '__main__':
    main()
