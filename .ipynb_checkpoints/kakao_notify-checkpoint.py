# kakao_notify.py

import pandas as pd
import requests
import logging





# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger()

CSV_FILE = 'data/kakao_users.csv'

# def load_data():
#     try:
#         return pd.read_csv(CSV_FILE, encoding='utf-8')
#     except UnicodeDecodeError:
#         return pd.read_csv(CSV_FILE, encoding='cp949')
#     except FileNotFoundError:
#         return pd.DataFrame(columns=['kakao_id', 'condition_value'])

# def load_data():
#     encodings = ['utf-8', 'cp949']
#     for encoding in encodings:
#         try:
#             data = pd.read_csv(CSV_FILE, encoding=encoding, on_bad_lines='skip')
#             logger.info(f"CSV file loaded successfully with {encoding} encoding.")
#             return data
#         except UnicodeDecodeError:
#             logger.warning(f"Failed to load CSV file with {encoding} encoding.")
#             continue
#         except Exception as e:
#             logger.error(f"Unexpected error occurred: {e}")
#     logger.error("Failed to load CSV file with all attempted encodings.")
#     return pd.DataFrame(columns=['kakao_id', 'condition_value'])

def load_data():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=['kakao_id', 'condition_value'])


def save_data(data):
    try:
        data.to_csv(CSV_FILE, index=False, encoding='utf-8')
        logger.info("CSV file saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save CSV file: {e}")

def add_user(kakao_id, condition_value):
    data = load_data()
    if kakao_id in data['kakao_id'].values:
        logger.warning(f"Attempt to add a duplicate KakaoTalk ID: {kakao_id}")
        return 'This KakaoTalk ID is already registered.'
    else:
        new_entry = pd.DataFrame({'kakao_id': [kakao_id], 'condition_value': [condition_value]})
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)
        logger.info(f"User added successfully: {kakao_id}")
        return 'User added successfully!'

def remove_user(kakao_id):
    data = load_data()
    if kakao_id in data['kakao_id'].values:
        data = data[data['kakao_id'] != kakao_id]
        save_data(data)
        logger.info(f"User removed successfully: {kakao_id}")
        return 'User removed successfully!'
    else:
        logger.warning(f"Attempt to remove a non-existent KakaoTalk ID: {kakao_id}")
        return 'KakaoTalk ID not found.'

def send_kakao_message(kakao_id, message):
    url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
    headers = {
        'Authorization': 'Bearer {ACCESS_TOKEN}',  # 발급받은 액세스 토큰을 입력합니다.
    }
    data = {
        'template_object': {
            'object_type': 'text',
            'text': message,
            'link': {
                'web_url': 'https://yourwebsite.com',
                'mobile_web_url': 'https://yourwebsite.com'
            }
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        logger.info(f"Message sent successfully to {kakao_id}")
        return 'Message sent successfully'
    else:
        logger.error(f"Failed to send message to {kakao_id}: {response.json()}")
        return 'Failed to send message'

def check_conditions_and_notify():
    data = load_data()
    for _, row in data.iterrows():
        if row['condition_value'] > 10:  # 조건을 필요에 따라 변경합니다.
            message = f'Condition met! Your input value is {row["condition_value"]}.'
            send_kakao_message(row['kakao_id'], message)
            logger.info(f"Notification sent to {row['kakao_id']}")
