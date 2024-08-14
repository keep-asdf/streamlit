import pandas as pd
import numpy as np
import pymysql

def alert_sys(df): 
    # 마지막 행 데이터 추출
    last_row = df.tail(1).iloc[0]
    
    # 기준치 설정
    concern_level = 5.0   # 관심
    warning_level = 7.0   # 주의
    alert_level = 8.0     # 경계
    critical_level = 9.2  # 심각
            
    # 알림 결과를 저장할 리스트
    alerts = []
    
    # 알림 조건 확인 및 메시지 생성
    if last_row['CI_Upper'] > concern_level and last_row['True_Value'] > last_row['CI_Upper']:
        alerts.append(f"미호천교 관심 알림!\n"
                      f"현재 시각 기준 3시간 후 ({last_row['Time']}) 예측된 미호천교 수위의 상방 신뢰구간이 "
                      f"{last_row['CI_Upper']}m로, 관심 수위 {concern_level}m를 초과합니다.")
    elif last_row['CI_Upper'] > warning_level and last_row['True_Value'] > last_row['CI_Upper']:
        alerts.append(f"미호천교 주의 알림!\n"
                      f"현재 시각 기준 3시간 후 ({last_row['Time']}) 예측된 미호천교 수위의 상방 신뢰구간이 "
                      f"{last_row['CI_Upper']}m로, 주의 수위 {warning_level}m를 초과합니다.")
    elif last_row['CI_Upper'] > alert_level and last_row['True_Value'] > last_row['CI_Upper']:
        alerts.append(f"미호천교 경계 알림!\n"
                      f"현재 시각 기준 3시간 후 ({last_row['Time']}) 예측된 미호천교 수위의 상방 신뢰구간이 "
                      f"{last_row['CI_Upper']}m로, 경계 수위 {alert_level}m를 초과합니다.")
    elif last_row['CI_Upper'] > critical_level and last_row['True_Value'] > last_row['CI_Upper']:
        alerts.append(f"미호천교 심각 알림!\n"
                      f"현재 시각 기준 3시간 후 ({last_row['Time']}) 예측된 미호천교 수위의 상방 신뢰구간이 "
                      f"{last_row['CI_Upper']}m로, 심각 수위 {critical_level}m를 초과합니다.")
    
    # 알림 메시지 리스트에 내용이 없으면 "현재, 안정적" 메시지 추가
    if not alerts:
        alerts.append(f"현재 시각 ({df.tail(4)['Time'].iloc[0]}) 미호천교 수위, 안정적 상태 ({df.tail(4)['True_Value'].iloc[0]}m) 입니다.")
    
    # 줄 바꿈을 포함한 하나의 문자열로 반환
    return "\n\n".join(alerts)
