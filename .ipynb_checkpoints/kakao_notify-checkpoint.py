##################################
####### EC2를 이용한 버전 #########
##################################


import pymysql
import logging
import pandas as pd
import streamlit as st
import requests 



# MySQL 데이터베이스 연결 설정
DB_HOST = '54.84.14.253'  # EC2 인스턴스의 퍼블릭 IP 주소
DB_USER = 'streamlit_user'
DB_PASSWORD = 'Streamlit_user1!'
DB_NAME = 'kakao_db'

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger()


    
# def get_db_connection():
#     try:
#         logger.debug(f"Attempting to connect to MySQL database at {DB_HOST} with user {DB_USER}")
#         connection = pymysql.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME,
#             charset='utf8mb4',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         logger.info("Database connection successful")
#         return connection
#     except pymysql.MySQLError as e:
#         logger.error(f"Database connection failed: {e}")
#         st.error("Failed to connect to the database. Check the logs for more details.")
#         return None
    
# def load_changes():
#     connection = get_db_connection()
#     if connection is None:
#         return pd.DataFrame()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM user_changes ORDER BY change_time DESC")
#             changes = cursor.fetchall()
#             return pd.DataFrame(changes)
#     finally:
#         if connection is not None:
#             connection.close()

# def load_data():
#     connection = get_db_connection()
#     if connection is None:
#         return pd.DataFrame()
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users")
#             data = cursor.fetchall()
#             return pd.DataFrame(data)
#     finally:
#         if connection is not None:
#             connection.close()

# def add_user(kakao_id, condition_value):
#     connection = get_db_connection()
#     if connection is None:
#         return 'Failed to connect to the database.'
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE kakao_id = %s", (kakao_id,))
#             result = cursor.fetchone()
#             if result:
#                 logger.warning(f"Attempt to add a duplicate KakaoTalk ID: {kakao_id}")
#                 return 'This KakaoTalk ID is already registered.'
#             else:
#                 cursor.execute(
#                     "INSERT INTO users (kakao_id, condition_value) VALUES (%s, %s)",
#                     (kakao_id, condition_value)
#                 )
#                 connection.commit()
#                 logger.info(f"User added successfully: {kakao_id}")
#                 return 'User added successfully!'
#     except Exception as e:
#         logger.error(f"Failed to add user: {e}")
#         return 'Failed to add user.'
#     finally:
#         if connection is not None:
#             connection.close()

# def remove_user(kakao_id):
#     connection = get_db_connection()
#     if connection is None:
#         return 'Failed to connect to the database.'
#     try:
#         with connection.cursor() as cursor:
#             logger.debug(f"Attempting to find user with kakao_id: {kakao_id}")
#             cursor.execute("SELECT * FROM users WHERE kakao_id = %s", (kakao_id,))
#             result = cursor.fetchone()
#             if result:
#                 logger.debug(f"User found: {result}")
#                 cursor.execute("DELETE FROM users WHERE kakao_id = %s", (kakao_id,))
#                 connection.commit()
#                 logger.info(f"User removed successfully: {kakao_id}")
#                 return 'User removed successfully!'
#             else:
#                 logger.warning(f"Attempt to remove a non-existent KakaoTalk ID: {kakao_id}")
#                 return 'KakaoTalk ID not found.'
#     except Exception as e:
#         logger.error(f"Failed to remove user: {e}")
#         return f'Failed to remove user: {e}'
#     finally:
#         if connection is not None:
#             connection.close()


# def send_kakao_message(kakao_id, message):
#     url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
#     headers = {
#         'Authorization': 'Bearer {ACCESS_TOKEN}',  # 발급받은 액세스 토큰을 입력합니다.
#     }
#     data = {
#         'template_object': {
#             'object_type': 'text',
#             'text': message,
#             'link': {
#                 'web_url': 'https://yourwebsite.com',
#                 'mobile_web_url': 'https://yourwebsite.com'
#             }
#         }
#     }

#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         logger.info(f"Message sent successfully to {kakao_id}")
#         return 'Message sent successfully'
#     else:
#         logger.error(f"Failed to send message to {kakao_id}: {response.json()}")
#         return 'Failed to send message'

# def check_conditions_and_notify():
#     data = load_data()
#     for _, row in data.iterrows():
#         if row['condition_value'] > 10:  # 조건을 필요에 따라 변경합니다.
#             message = f'Condition met! Your input value is {row["condition_value"]}.'
#             send_kakao_message(row['kakao_id'], message)
#             logger.info(f"Notification sent to {row['kakao_id']}")

def get_db_connection(retries=5, delay=5):
    for attempt in range(retries):
        try:
            logger.debug(f"Attempting to connect to MySQL database at {DB_HOST} with user {DB_USER}")
            connection = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            logger.info("Database connection successful")
            return connection
        except pymysql.MySQLError as e:
            logger.error(f"Database connection failed (attempt {attempt + 1} of {retries}): {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                st.error(f"Failed to connect to the database after {retries} attempts. Error: {e}")
                return None

            
def load_changes():
    connection = get_db_connection()
    if connection is None:
        return pd.DataFrame()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_changes ORDER BY change_time DESC")
            changes = cursor.fetchall()
            return pd.DataFrame(changes)
    finally:
        if connection is not None:
            connection.close()

def load_data():
    connection = get_db_connection()
    if connection is None:
        return pd.DataFrame()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            data = cursor.fetchall()
            return pd.DataFrame(data)
    finally:
        if connection is not None:
            connection.close()

def add_user(kakao_id, condition_value):
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database.'
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE kakao_id = %s", (kakao_id,))
            result = cursor.fetchone()
            if result:
                logger.warning(f"Attempt to add a duplicate KakaoTalk ID: {kakao_id}")
                return 'This KakaoTalk ID is already registered.'
            else:
                cursor.execute(
                    "INSERT INTO users (kakao_id, condition_value) VALUES (%s, %s)",
                    (kakao_id, condition_value)
                )
                connection.commit()
                logger.info(f"User added successfully: {kakao_id}")
                return 'User added successfully!'
    except Exception as e:
        logger.error(f"Failed to add user: {e}")
        return f'Failed to add user: {e}'
    finally:
        if connection is not None:
            connection.close()

def remove_user(kakao_id):
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database.'
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE kakao_id = %s", (kakao_id,))
            result = cursor.fetchone()
            if result:
                cursor.execute("DELETE FROM users WHERE kakao_id = %s", (kakao_id,))
                connection.commit()
                logger.info(f"User removed successfully: {kakao_id}")
                return 'User removed successfully!'
            else:
                logger.warning(f"Attempt to remove a non-existent KakaoTalk ID: {kakao_id}")
                return 'KakaoTalk ID not found.'
    except Exception as e:
        logger.error(f"Failed to remove user: {e}")
        return f'Failed to remove user: {e}'
    finally:
        if connection is not None:
            connection.close()

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
