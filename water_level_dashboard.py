import streamlit as st
from visualizations import *
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

import datetime

import pydeck as pdk


st.set_page_config(layout="wide")

# Streamlit app
def main():
    
    # UTC 기준의 현재 시간을 얻습니다.
    current_time_utc = datetime.datetime.utcnow()

    # 서울시간 (UTC+9)을 고려하여 9시간을 더합니다.
    current_time_seoul = current_time_utc + datetime.timedelta(hours=9)

    # 현재 시간의 "시" 값을 가져옵니다.
    current_hour_seoul = current_time_seoul.hour
    current_hour_seoul_full = current_time_seoul.strftime("%Y-%m-%d %H")
    st.title(f"💧❕ 미호천교 {current_hour_seoul}:00(24H) 기준, 3시간 후 수위 예측 Dashboard")
    # st.title(f"(❗현재{current_hour_seoul_full}:00(24H), 미호천교 재방 공사로 인해, 수위 데이터 측정 중단)")
    # st.title("(❗따라서 수위 데이터 측정 재개 전까지 예측을 일시 중단합니다.)")

    # 사이드바에 버튼을 추가합니다.
    update_button = st.sidebar.button("Update Data")
    
    
    # 사이드바를 사용하여 그래프 선택
    # graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

    
    # 사이드바를 사용하여 그래프 선택
    with st.sidebar:
        choice = option_menu("Menu", ["Prediction Result", "True vs Predicted with CI"])
    

    ####################################################################################
    ####################################################################################
    ####################################################################################
    if choice == "Prediction Result":
        
        with st.container():
            
           # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_data_moving_averages():
                return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

            data_moving_averages = load_data_moving_averages()

            # Convert the 'Time' column to datetime format
            data_moving_averages['Time'] = pd.to_datetime(data_moving_averages['Time'])

            # Check the last 6 hours of data
            last_6h_data = data_moving_averages.loc[data_moving_averages['Time'] >= data_moving_averages['Time'].iloc[-1] - pd.Timedelta(hours=6)]

            
             ##################################################################
            # Streamlit에서 날짜와 시간을 입력받습니다.
            col1, col2 = st.columns(2)
            with col1:
                


                selected_date1 = st.date_input("Select a date", datetime.date.today())
            
            with col2:
                
                hours_list = [f"{i:02d}:00" for i in range(24)]  # ["00:00", "01:00", ... , "23:00"]
                selected_hour_str = st.selectbox("Select an hour", hours_list, index=12)  # 초기값은 "12:00"
                selected_time1 = int(selected_hour_str.split(":")[0])  # 문자열에서 시간 부분만 추출하여 정수로 변환

                
            show_blue_line1 = st.checkbox("Show blue guide line at selected time", True)  # 기본값으로 체크 상태

            
            selected_datetime1 = datetime.datetime.combine(selected_date1, datetime.time(selected_time1, 0))  # 날짜와 시간 결합
            
            
            ##################################################################
            
            
            st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages, selected_datetime1, show_blue_line1))
            
            
            
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
        
        
            #traffic data 표시 및 지도 표시
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_traffic_data():
                return pd.read_csv('data/traffic_data.csv').copy()

            traffic_df = load_traffic_data()
            
            
            # 기준 좌표를 데이터 프레임에 추가
            new_data = {
                'type' : '미호천교 기준 좌표',
                'coordX': [36.6230541816206],
                'coordY': [127.35070148286204]
            }
            new_df = pd.DataFrame(new_data)

            # 데이터 프레임에 새로운 행을 추가
            traffic_df = pd.concat([traffic_df, new_df], ignore_index=True)

            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("실시간 미호천교 근방 교통 이벤트 데이터\n(empty = 현재 이벤트 없음)")
                st.write(traffic_df)
            
            with col2:
                st.map(traffic_df,latitude = 'coordX', longitude = 'coordY', color = '#8B0000', size = 10)
                

    ###################################################################################
    ###################################################################################
    ###################################################################################
    elif choice == "True vs Predicted with CI":
        
        placeholder = st.empty()
        with placeholder.container():
            
            # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_data_true_pred():
                return pd.read_csv('data/true_pred_with_CI.csv').copy()

            data_true_pred = load_data_true_pred()
            
             ##################################################################
            # Streamlit에서 날짜와 시간을 입력받습니다.
            col1, col2 = st.columns(2)
            with col1:

                selected_date2 = st.date_input("Select a date", datetime.date.today())
            
            with col2:
                                
                hours_list = [f"{i:02d}:00" for i in range(24)]  # ["00:00", "01:00", ... , "23:00"]
                selected_hour_str = st.selectbox("Select an hour", hours_list, index=12)  # 초기값은 "12:00"
                selected_time2 = int(selected_hour_str.split(":")[0])  # 문자열에서 시간 부분만 추출하여 정수로 변환

                
            show_blue_line2 = st.checkbox("Show blue guide line at selected time", True)  # 기본값으로 체크 상태

            
            selected_datetime2 = datetime.datetime.combine(selected_date2, datetime.time(selected_time2, 0))  # 날짜와 시간 결합
            
            
            ##################################################################
            
            st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred, selected_datetime2, show_blue_line2))


            
            data_true_pred = load_data_true_pred()

            data_true_pred['Time'] = pd.to_datetime(data_true_pred['Time'])

            # Check the last 6 hours of data
            true_pred_last_6h_data = data_true_pred.loc[data_true_pred['Time'] >= data_true_pred['Time'].iloc[-1] - pd.Timedelta(hours=6)]

             # 데이터 프레임과 그래프를 나란히 표시
            col1, col2 = st.columns(2)
            with col1:
                st.write(data_true_pred.sort_values(by='Time', ascending=False))
            with col2:
                st.bokeh_chart(visualize_true_vs_predicted_last_6h(true_pred_last_6h_data))\



if __name__ == '__main__':
    main()
