##################################
####### EC2를 이용한 버전 #########
##################################


import pymysql
import logging
import pandas as pd
import streamlit as st
import requests 
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re  # re 모듈을 임포트합니다.


# MySQL 데이터베이스 연결 설정
DB_HOST = st.secrets["database"]["DB_HOST"]
DB_USER = st.secrets["database"]["DB_USER"]
DB_PASSWORD = st.secrets["database"]["DB_PASSWORD"]
DB_NAME = st.secrets["database"]["DB_NAME"]


# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='app.log', filemode='a')
logger = logging.getLogger()

# 이메일 설정
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP 서버
EMAIL_PORT = 587
EMAIL_USER = st.secrets["email"]["user"]
EMAIL_PASSWORD = st.secrets["email"]["password"]


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
            
            

def add_user(e_mail_address):
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database.'
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE e_mail_address = %s", (e_mail_address,))
            result = cursor.fetchone()
            if result:
                logger.warning(f"Attempt to add a duplicate KakaoTalk ID: {e_mail_address}")
                return 'This KakaoTalk ID is already registered.'
            else:
                cursor.execute(
                    "INSERT INTO users (e_mail_address) VALUES (%s, %s)",
                    (e_mail_address)
                )
                connection.commit()
                logger.info(f"User added successfully: {e_mail_address}")
                return 'User added successfully!'
    except Exception as e:
        logger.error(f"Failed to add user: {e}")
        return f'Failed to add user: {e}'
    finally:
        if connection is not None:
            connection.close()

def remove_user(e_mail_address):
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database.'
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE e_mail_address = %s", (e_mail_address,))
            result = cursor.fetchone()
            if result:
                cursor.execute("DELETE FROM users WHERE e_mail_address = %s", (e_mail_address,))
                connection.commit()
                logger.info(f"User removed successfully: {e_mail_address}")
                return 'User removed successfully!'
            else:
                logger.warning(f"Attempt to remove a non-existent KakaoTalk ID: {e_mail_address}")
                return 'KakaoTalk ID not found.'
    except Exception as e:
        logger.error(f"Failed to remove user: {e}")
        return f'Failed to remove user: {e}'
    finally:
        if connection is not None:
            connection.close()

            
# 이메일 전송 함수
def send_email(subject, 
               body, 
               to_email, 
               EMAIL_USER = EMAIL_USER, 
               EMAIL_PASSWORD = EMAIL_PASSWORD):
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        return 'Email sent successfully'
    except smtplib.SMTPAuthenticationError as e:
        return f"Failed to authenticate: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

    
    
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
#             send_kakao_message(row['e_mail_address'], message)
#             logger.info(f"Notification sent to {row['e_mail_address']}")

            
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None