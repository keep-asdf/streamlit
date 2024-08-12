import streamlit as st
from visualizations import *
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import datetime
import pydeck as pdk
from kakao_notify import *
from bokeh.layouts import gridplot
from bokeh.layouts import column, row


import streamlit as st
from PIL import Image
import os




st.set_page_config(layout="wide")

# 관리자 비밀번호 설정
ADMIN_PASSWORD = "1234"


# Streamlit app
def main():

    
# ################################################
#     # 관리자 인증
#     if 'authenticated' not in st.session_state:
#         st.session_state['authenticated'] = False

#     if not st.session_state['authenticated']:
#         password = st.text_input("Enter admin password:", type="password")
#         if st.button("Login"):
#             if password == ADMIN_PASSWORD:
#                 st.session_state['authenticated'] = True
#                 st.success("Login successful")
#             else:
#                 st.error("Invalid password")
#         return
# ################################################
    
    
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
    # update_button = st.sidebar.button("Update Data")
    update_button = st.sidebar.button("Update Data", key="update_data_button")

    
    # 사이드바를 사용하여 그래프 선택
    # graph_selection = st.sidebar.selectbox("Choose a Graph", ["Moving Averages", "True vs Predicted with CI"])

    
    # 사이드바를 사용하여 그래프 선택
    with st.sidebar:
        
        # choice = option_menu("Menu", ["Prediction Result", 
        # "True vs Predicted with CI", 
        # "Test", "Kakao Notification"])
        
        
        # choice = option_menu("Menu", ["Prediction Result", 
        # "True vs Predicted with CI", "Test", 
        # "Kakao Notification", 
        # "Admin Page"])
        
        
        # choice = option_menu("Menu", ["Prediction Result", 
        # "True vs Predicted with CI", 
        # "Test", 
        # "Kakao Notification", 
        # "Admin Page"], key="menu")
        
        
        # choice = option_menu("Menu", ["True vs Predicted with CI(Random Forest ver)", 
#         "True vs Predicted with Uncertainty(Bayesian LSTM ver)", 
#         "Kakao Notification", 
#         "Admin Page"], 
#         key="menu")
        
    
        choice = option_menu("Menu", ["Introduction", 
                                      "True vs Predicted with CI(Random Forest ver)",  
                                      "True vs Predicted with Uncertainty(Bayesian LSTM ver)",
                                      "Email Notification", "Admin Page"], 
                             key="menu")

    
    ####################################################################################
    ####################################################################################
    ####################################################################################

    if choice == "Introduction":

        with st.container():
            # 이미지 파일 경로
            image_path = "data/daemoon.jpg"

            # HTML과 CSS를 사용하여 이미지를 중앙에 배치
            st.markdown(
                f"""
                
                <div style="display: flex; 
                justify-content: center; 
                align-items: center; 
                height: auto;">
                
                <img src="{image_path}"
                alt="Sample Image" 
                style="max-width:100%;
                height:auto;">
                
                </div>
                """,
                
                unsafe_allow_html=True
                )




            
            
    
    elif choice == "True vs Predicted with CI(Random Forest ver)":
        
        with st.container():
            
           # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            
#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_data_moving_averages():
#                 return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

#             data_moving_averages = load_data_moving_averages()
            
            # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_data_true_pred():
                return pd.read_csv('data/true_pred_with_CI.csv').copy()

            data_true_pred = load_data_true_pred()
            
            
            # Convert the 'Time' column to datetime format
            data_true_pred['Time'] = pd.to_datetime(data_true_pred['Time'])

            # Check the last 6 hours of data
            true_pred_last_6h_data = data_true_pred.loc[data_true_pred['Time'] >= data_true_pred['Time'].iloc[-1] - pd.Timedelta(hours=6)]

            

            
            
             ##################################################################
            # Streamlit에서 날짜와 시간을 입력받습니다.
            col1, col2 = st.columns(2)
            with col1:

                selected_date1 = st.date_input("Select a date", datetime.date.today())
            
            with col2:
                # ["00:00", "01:00", ... , "23:00"]
                hours_list = [f"{i:02d}:00" for i in range(24)]  
                # 초기값은 "12:00"
                selected_hour_str = st.selectbox("Select an hour", hours_list, index=12) 
                # 문자열에서 시간 부분만 추출하여 정수로 변환
                selected_time1 = int(selected_hour_str.split(":")[0])  

            # 기본값으로 체크 상태    
            show_blue_line1 = st.checkbox("Show blue guide line at selected time", True)  
            # 날짜와 시간 결합
            selected_datetime1 = datetime.datetime.combine(selected_date1,
                                                           datetime.time(selected_time1, 0)) 
                
            
            
            ##################################################################
            
            
            # st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages, selected_datetime1, show_blue_line1))
            
            st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred,
                                                                              selected_datetime1,
                                                                              show_blue_line1))        
            
            
             # 데이터 프레임과 그래프를 나란히 표시
            col1, col2 = st.columns(2)
            with col1:
                # st.write(data_moving_averages.sort_values(by='Time', ascending=False))
                st.write(data_true_pred.sort_values(by='Time', ascending=False))
                # st.dataframe(data_true_pred.sort_values(by='Time', 
                #                                         ascending=False).head(1000), 
                #                                         use_container_width=True)



            with col2:
                st.bokeh_chart(visualize_true_vs_predicted_last_6h(true_pred_last_6h_data))

                
                
#####
#########################

#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_water_data():
#                 return pd.read_csv('data/water_data.csv').copy()
       
#             data_water_data = load_water_data().copy()
#             # 각 feature에 대한 그래프 생성
#             graphs = create_individual_graphs(data_water_data)
        
#             # 2x3 그리드로 그래프 표시
#             grid = gridplot([graphs[:3], graphs[3:]])
#             st.bokeh_chart(grid)       
        
        

#              # Streamlit에서 사용
#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_water_data():
#                 return pd.read_csv('data/water_data.csv').copy()

#             data_water_data = load_water_data().copy()

#             # 각 feature에 대한 그래프 생성
#             graphs = create_individual_graphs(data_water_data)

#             # 그래프를 2x3 형태로 배치하는 대신 column과 row를 활용하여 동적으로 배치
#             layout = column(
#                 row(graphs[0], graphs[1]),  # 여기서는 각 그래프의 크기를 자동 조정합니다.
#                 row(graphs[2], graphs[3], graphs[4])  # 남은 그래프도 같은 방식으로 배치
#             )

#             st.bokeh_chart(layout, use_container_width=True)


            # Streamlit에서 사용
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_water_data():
                return pd.read_csv('data/water_data.csv').copy()

            data_water_data = load_water_data().copy()

            # 각 feature에 대한 그래프 생성
            graphs = create_individual_graphs(data_water_data)

            # 그래프를 2x3 형태로 배치하는 대신 column과 row를 활용하여 동적으로 배치
            layout = gridplot(graphs, ncols=3, 
                              sizing_mode="scale_both")

            st.bokeh_chart(layout, 
                           use_container_width=True)

        
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
            traffic_df = pd.concat([traffic_df, new_df], 
                                   ignore_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("실시간 미호천교 근방 교통 이벤트 데이터\n(empty = 현재 이벤트 없음)")
                st.write(traffic_df)
            
            with col2:
                st.map(traffic_df,latitude = 'coordX',
                       longitude = 'coordY', 
                       color = '#8B0000', 
                       size = 10)
                


                

                
#    ####################################################################################
#     if choice == "Prediction Result":
        
#         with st.container():
            
#            # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            
#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_data_moving_averages():
#                 return pd.read_csv('data/water_level_with_moving_averages.csv').copy()

#             data_moving_averages = load_data_moving_averages()

#             # Convert the 'Time' column to datetime format
#             data_moving_averages['Time'] = pd.to_datetime(data_moving_averages['Time'])

#             # Check the last 6 hours of data
#             last_6h_data = data_moving_averages.loc[data_moving_averages['Time'] >= data_moving_averages['Time'].iloc[-1] - pd.Timedelta(hours=6)]

            
#              ##################################################################
#             # Streamlit에서 날짜와 시간을 입력받습니다.
#             col1, col2 = st.columns(2)
#             with col1:

#                 selected_date1 = st.date_input("Select a date", datetime.date.today())
            
#             with col2:
                
#                 hours_list = [f"{i:02d}:00" for i in range(24)]  # ["00:00", "01:00", ... , "23:00"]
#                 selected_hour_str = st.selectbox("Select an hour", hours_list, index=12)  # 초기값은 "12:00"
#                 selected_time1 = int(selected_hour_str.split(":")[0])  # 문자열에서 시간 부분만 추출하여 정수로 변환

                
#             show_blue_line1 = st.checkbox("Show blue guide line at selected time", True)  # 기본값으로 체크 상태

            
#             selected_datetime1 = datetime.datetime.combine(selected_date1, datetime.time(selected_time1, 0))  # 날짜와 시간 결합
            
            
#             ##################################################################
            
            
#             st.bokeh_chart(visualize_moving_averages_with_bokeh(data_moving_averages, selected_datetime1, show_blue_line1))
            
            
            
#              # 데이터 프레임과 그래프를 나란히 표시
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.write(data_moving_averages.sort_values(by='Time', ascending=False))
#             with col2:
#                 st.bokeh_chart(visualize_last_6h_moving_averages(last_6h_data))

                
                
# #####


#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_water_data():
#                 return pd.read_csv('data/water_data.csv').copy()
       
#             data_water_data = load_water_data().copy()
#             # 각 feature에 대한 그래프 생성
#             graphs = create_individual_graphs(data_water_data)
        
#             # 2x3 그리드로 그래프 표시
#             grid = gridplot([graphs[:3], graphs[3:]])
#             st.bokeh_chart(grid)       
        
        
#             #traffic data 표시 및 지도 표시
#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_traffic_data():
#                 return pd.read_csv('data/traffic_data.csv').copy()

#             traffic_df = load_traffic_data()
            
            
#             # 기준 좌표를 데이터 프레임에 추가
#             new_data = {
#                 'type' : '미호천교 기준 좌표',
#                 'coordX': [36.6230541816206],
#                 'coordY': [127.35070148286204]
#             }
#             new_df = pd.DataFrame(new_data)

#             # 데이터 프레임에 새로운 행을 추가
#             traffic_df = pd.concat([traffic_df, new_df], ignore_index=True)

            
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.subheader("실시간 미호천교 근방 교통 이벤트 데이터\n(empty = 현재 이벤트 없음)")
#                 st.write(traffic_df)
            
#             with col2:
#                 st.map(traffic_df,latitude = 'coordX', longitude = 'coordY', color = '#8B0000', size = 10)
                

#     ###################################################################################
#     ###################################################################################
#     ###################################################################################
#     elif choice == "True vs Predicted with CI":
        
#         placeholder = st.empty()
#         with placeholder.container():
            
#             # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
#             @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
#             def load_data_true_pred():
#                 return pd.read_csv('data/true_pred_with_CI.csv').copy()

#             data_true_pred = load_data_true_pred()
            
#              ##################################################################
#             # Streamlit에서 날짜와 시간을 입력받습니다.
#             col1, col2 = st.columns(2)
#             with col1:

#                 selected_date2 = st.date_input("Select a date", datetime.date.today())
            
#             with col2:
                                
#                 hours_list = [f"{i:02d}:00" for i in range(24)]  # ["00:00", "01:00", ... , "23:00"]
#                 selected_hour_str = st.selectbox("Select an hour", hours_list, index=12)  # 초기값은 "12:00"
#                 selected_time2 = int(selected_hour_str.split(":")[0])  # 문자열에서 시간 부분만 추출하여 정수로 변환

                
#             show_blue_line2 = st.checkbox("Show blue guide line at selected time", True)  # 기본값으로 체크 상태

            
#             selected_datetime2 = datetime.datetime.combine(selected_date2, datetime.time(selected_time2, 0))  # 날짜와 시간 결합
            
            
#             ##################################################################
            
#             st.bokeh_chart(visualize_true_pred_with_CI_and_status_lines_bokeh(data_true_pred,selected_datetime2, show_blue_line2))


            
#             data_true_pred = load_data_true_pred()

#             data_true_pred['Time'] = pd.to_datetime(data_true_pred['Time'])

#             # Check the last 6 hours of data
#             true_pred_last_6h_data = data_true_pred.loc[data_true_pred['Time'] >= data_true_pred['Time'].iloc[-1] - pd.Timedelta(hours=6)]

#              # 데이터 프레임과 그래프를 나란히 표시
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.write(data_true_pred.sort_values(by='Time', ascending=False))
#             with col2:
#                 st.bokeh_chart(visualize_true_vs_predicted_last_6h(true_pred_last_6h_data))
                


   ###################################################################################
    ###################################################################################
    ###################################################################################
    elif choice == "True vs Predicted with Uncertainty(Bayesian LSTM ver)":
        
        placeholder = st.empty()
        with placeholder.container():
            
            # 데이터를 로드합니다. 캐시는 1시간마다 만료됩니다.
            # @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            # def load_data_pred_uncer():
            #     return pd.read_csv('data/bayes_pred_uncer.csv').copy()
            
            @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            def load_data_total():
                return pd.read_csv('data/new_new_data.csv').copy()
            
            # pred_uncer = load_data_pred_uncer().copy()
            bayes_data = load_data_total().copy()
            
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
                  
            
                        
            st.bokeh_chart(plot_predictions_with_uncertainty_bokeh(bayes_data, 
                                                                   selected_datetime=selected_datetime2,
                                                                   show_blue_line = show_blue_line2),
                           use_container_width=True)
            
            ##################################################################

            
            # @st.cache_data(ttl=3600)  # 3600 seconds = 1 hour
            # def load_ppd_data():
            #     return pd.read_csv('data/bayesian_ppd_visual.csv').copy()
       
            # ppd_data = load_ppd_data()
            time_points_to_plot = bayes_data['Time'].unique()[-3:]            
            st.bokeh_chart(plot_posterior_predictive_distribution_bokeh(bayes_data,
                                                                        time_points_to_plot),
                                                use_container_width=True,
                          )            
            
            # st.write(pred_uncer.sort_values(by='Time', ascending=False))
            
            # st.dataframe(pred_uncer.sort_values(by='Time', ascending=False), width=1000)   
#             st.dataframe(pred_uncer.sort_values(by='Time', 
#                                                 ascending=False), 
#                         use_container_width=True)
            
            st.dataframe(bayes_data.iloc[:, 0:6].sort_values(by='Time', 
                                                ascending=False), 
                        use_container_width=True)
#             data_true_pred = load_data_pred_uncer()

#             data_true_pred['Time'] = pd.to_datetime(data_true_pred['Time'])
            
            
            
#             @st.cache_data(ttl=3600)
#             def load_data_predicted_volatility():
#                 return pd.read_csv('data/volatility.csv').copy()

#             data_predicted_volatility = load_data_predicted_volatility()
#             fig = plot_predicted_volatility(data_predicted_volatility)
#             st.pyplot(fig)

                           
                           
                           
                           
                           
                           
#     ###################################################################################
#     ###################################################################################
#     ###################################################################################
#     elif choice == "Kakao Notification":
#         st.subheader("KakaoTalk Notification System")
        
#         kakao_id = st.text_input('Enter KakaoTalk ID:')
#         condition_value = st.number_input('Enter condition value:', min_value=0, max_value=100)

#         if st.button('Add/Update User'):
#             result = add_user(kakao_id, condition_value)
#             st.success(result) if 'successfully' in result else st.warning(result)

#         if st.button('Remove User'):
#             result = remove_user(kakao_id)
#             st.success(result) if 'removed successfully' in result else st.warning(result)

#         if st.button('Check Conditions and Notify'):
#             check_conditions_and_notify()

#         # # 등록된 사용자 목록을 관리자만 볼 수 있도록 설정
#         # if st.session_state['authenticated']:
#         #     st.subheader('Registered Users')
#         #     data = load_data()
#         #     st.write(data)
        
#        # 등록된 사용자 목록을 표시합니다.
#         st.subheader('Registered Users')
#         data = load_data()
#         st.write(data)
    ###################################################################################
    ###################################################################################
    ###################################################################################
#     # Kakao Notification 페이지
#     elif choice == "Email Notification":
#         st.subheader("KakaoTalk Notification System")
        
#         kakao_id = st.text_input('Enter KakaoTalk ID:', key="kakao_id_input")
#         condition_value = st.number_input('Enter condition value (set the condition to trigger the notification):', min_value=0, max_value=100, key="condition_value_input")
    
# #         if st.button('Add/Update User', key="add_update_user"):
# #             result = add_user(kakao_id, condition_value)
# #             st.success(result) if 'successfully' in result else st.warning(result)
    
# #         if st.button('Remove User', key="remove_user"):
# #             result = remove_user(kakao_id)
# #             st.success(result) if 'removed successfully' in result else st.warning(result)
    
# #         if st.button('Check Conditions and Notify', key="check_conditions"):
# #             check_conditions_and_notify()

#         if st.button('Add/Update User', key="add_update_user_button"):
#             result = add_user(kakao_id, condition_value)
#             if 'successfully' in result:
#                 st.success(result)
#             else:
#                 st.warning(result)
        
#         if st.button('Remove User', key="remove_user_button"):
#             result = remove_user(kakao_id)
#             if 'removed successfully' in result:
#                 st.success(result)
#             else:
#                 st.warning(result)
        
#         if st.button('Check Conditions and Notify', key="check_conditions_button"):
#             check_conditions_and_notify()
#             st.success("Checked conditions and sent notifications if any.")
        
    # Kakao Notification 페이지
    elif choice == "Email Notification":
        st.subheader("Email Notification System")
        
        email_address = st.text_input('Enter Email Address:', 
                                      key="email_address_input")
        condition_value = st.number_input('Enter condition value (set the condition to trigger the notification):', min_value=0, max_value=100, key="condition_value_input")
    

        if st.button('Add/Update User', key="add_update_user_button"):
            result = add_user(email_address, condition_value)
            if 'successfully' in result:
                st.success(result)
            else:
                st.warning(result)
        
        if st.button('Remove User', key="remove_user_button"):
            result = remove_user(email_address)
            if 'removed successfully' in result:
                st.success(result)
            else:
                st.warning(result)
        
        if st.button('Check Conditions and Notify', key="check_conditions_button"):
            check_conditions_and_notify()
            st.success("Checked conditions and sent notifications if any.")
        
        # 이메일 테스트 기능 추가
        if st.button('Test Email', key="test_email_button"):
            
            test_subject = "Test Notification"
            test_body = "This is a test email to verify the notification system."
            test_result = send_email(test_subject, test_body, email_address)
        
            if 'successfully' in test_result:
                st.success(f"Test email sent successfully to {email_address}")
            else:
                st.warning(f"Failed to send test email: {test_result}")
        


    ###################################################################################
    ###################################################################################
    
    
    elif choice == "Admin Page":
        st.subheader("Admin Page")
    
        # 관리자 인증
        if 'authenticated' not in st.session_state:
            st.session_state['authenticated'] = False
    
        if not st.session_state['authenticated']:
            password = st.text_input("Enter admin password:", 
                                     type="password", 
                                     key="admin_password_input")
            if st.button("Login", key="admin_login_button"):
                if password == ADMIN_PASSWORD:
                    st.session_state['authenticated'] = True
                    st.success("Login successful")
                    # st.experimental_rerun()  # 로그인 성공 시 페이지 새로고침
                else:
                    st.error("Invalid password")
            return
    
        # 관리자 인증 후 표시할 내용
        if st.session_state['authenticated']:
            st.subheader('Registered Users')
            
            ##
            # if st.button("Load KakaoTalk User List", key="load_kakao_user_list"):
            #     data = load_data()
            #     st.write(data)
            ##
            
            if st.button("Load Data and Changes", 
                         key="load_data_and_changes"):
                
                data = load_data()
                st.write("Current Data:")
                st.write(data)
                
                changes = load_changes()
                st.write("Change Log:")
                st.write(changes)
            
            
#             # 로그 파일 읽기
#             log_file = 'logs/app.log'
#             st.subheader('Application Logs')
#             try:
#                 with open(log_file, 'r') as f:
#                     log_content = f.read()
#                     st.text(log_content)
#             except FileNotFoundError:
#                 st.error("Log file not found")
    

if __name__ == '__main__':
    main()
