import pandas as pd
import numpy as np
import streamlit as st  # st를 사용하기 위해 streamlit 모듈을 임포트해야 합니다.

def alert_sys(df): 
    # 마지막 4시간 데이터 추출
    last_4_hours_data = df.tail(4)      
    
    # 기준치 설정
    warning_level = 7.0  # 주의
    alert_level = 8.0    # 경계
    critical_level = 9.2  # 심각
            
    # 알림 조건 확인 및 표시
    for index, row in last_4_hours_data.iterrows():
        if row['CI_Upper'] > critical_level and row['True_Value'] > row['CI_Upper']:
            st.error(f"심각 경보! 시간: {row['Time']}, "
                     f"True Value: {row['True_Value']}, "
                     f"Upper CI: {row['CI_Upper']}")
                     
        elif row['CI_Upper'] > alert_level and row['True_Value'] > row['CI_Upper']:
            st.warning(f"경계 경보! 시간: {row['Time']}, "
                       f"True Value: {row['True_Value']}, "
                       f"Upper CI: {row['CI_Upper']}")
                       
        elif row['CI_Upper'] > warning_level and row['True_Value'] > row['CI_Upper']:
            st.info(f"주의 경보! 시간: {row['Time']}, "
                    f"True Value: {row['True_Value']}, "
                    f"Upper CI: {row['CI_Upper']}")
