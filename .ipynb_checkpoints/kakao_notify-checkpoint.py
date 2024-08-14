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
import random
import string
import datetime

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



# def get_email_addresses():
#     # MySQL 연결 설정
#     connection = pymysql.connect(
#                       host=DB_HOST,
#                       user=DB_USER,
#                       password=DB_PASSWORD,
#                       database=DB_NAME,
#                       charset='utf8mb4',
#                       cursorclass=pymysql.cursors.DictCursor
#                         )

#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT e_mail_address FROM users")
#             result = cursor.fetchall()
#             email_addresses = [row[0] for row in result]
#     finally:
#         connection.close()

#     return email_addresses

    
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
            
            

# def add_user(e_mail_address):
#     connection = get_db_connection()
#     if connection is None:
#         return 'Failed to connect to the database.'
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE e_mail_address = %s", (e_mail_address,))
#             result = cursor.fetchone()
#             if result:
#                 logger.warning(f"Attempt to add a duplicate KakaoTalk ID: {e_mail_address}")
#                 return 'This KakaoTalk ID is already registered.'
#             else:
#                 cursor.execute(
#                     "INSERT INTO users (e_mail_address) VALUES (%s, %s)",
#                     (e_mail_address)
#                 )
#                 connection.commit()
#                 logger.info(f"User added successfully: {e_mail_address}")
#                 return 'User added successfully!'
#     except Exception as e:
#         logger.error(f"Failed to add user: {e}")
#         return f'Failed to add user: {e}'
#     finally:
#         if connection is not None:
#             connection.close()

def add_user(e_mail_address):
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database.'
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE e_mail_address = %s", (e_mail_address,))
            result = cursor.fetchone()
            if result:
                logger.warning(f"Attempt to add a duplicate Email: {e_mail_address}")
                return 'This Email is already registered.'
            else:
                cursor.execute(
                    "INSERT INTO users (e_mail_address) VALUES (%s)",
                    (e_mail_address,)
                )
                connection.commit()
                logger.info(f"Email added successfully: {e_mail_address}")
                log_user_change('INSERT', e_mail_address)  # 로그 기록 추가
                return 'Email added successfully!'
    except Exception as e:
        logger.error(f"Failed to add Email: {e}")
        return f'Failed to add Email: {e}'
    finally:
        if connection is not None:
            connection.close()

# def remove_user(e_mail_address):
#     connection = get_db_connection()
#     if connection is None:
#         return 'Failed to connect to the database.'
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM users WHERE e_mail_address = %s", (e_mail_address,))
#             result = cursor.fetchone()
#             if result:
#                 cursor.execute("DELETE FROM users WHERE e_mail_address = %s", (e_mail_address,))
#                 connection.commit()
#                 logger.info(f"User removed successfully: {e_mail_address}")
#                 return 'User removed successfully!'
#             else:
#                 logger.warning(f"Attempt to remove a non-existent KakaoTalk ID: {e_mail_address}")
#                 return 'KakaoTalk ID not found.'
#     except Exception as e:
#         logger.error(f"Failed to remove user: {e}")
#         return f'Failed to remove user: {e}'
#     finally:
#         if connection is not None:
#             connection.close()


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
                logger.info(f"Email removed successfully: {e_mail_address}")
                log_user_change('DELETE', e_mail_address)  # 로그 기록 추가
                return '성공적으로 이메일을 등록취소 하였습니다!'
            else:
                logger.warning(f"Attempt to remove a non-existent Email: {e_mail_address}")
                return 'KakaoTalk ID not found.'
    except Exception as e:
        logger.error(f"Failed to remove Email: {e}")
        return f'Failed to remove Email: {e}'
    finally:
        if connection is not None:
            connection.close()

            
# 이메일 전송 함수
def send_email(subject, 
               body, 
               to_email, d
               EMAIL_USER = EMAIL_USER, 
               EMAIL_PASSWORD = EMAIL_PASSWORD):
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

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

    
            
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None


#####################################
#####################################
######## email 인증 관련 함수 ######## 
#####################################
#####################################

# 인증 코드 생성 함수
def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# 인증 코드를 데이터베이스에 저장하는 함수
def save_verification_code(email, code):
    expires_at = datetime.datetime.now() + datetime.timedelta(minutes=10)  # 만료 시간 설정 (10분 후)
    
    connection = get_db_connection()  # DB 연결
    cursor = connection.cursor()
    
    # 기존 인증 코드 삭제 (이미 있는 경우)
    cursor.execute("DELETE FROM email_verifications WHERE e_mail_address = %s", (email,))
    
    # 새로운 인증 코드 저장
    cursor.execute("""
        INSERT INTO email_verifications (e_mail_address, verification_code, expires_at)
        VALUES (%s, %s, %s)
    """, (email, code, expires_at))
    
    connection.commit()
    cursor.close()
    connection.close()

# 인증 코드를 이메일로 발송하는 함수
def send_verification_email(email):
    code = generate_verification_code()
    save_verification_code(email, code)
    
    subject = "이메일 인증 코드"
    body = f"귀하의 인증 코드는: {code} 입니다. 10분 내에 입력해주세요."
    
    return send_email(subject, body, email)


# 인증 코드를 검증하는 함수
# def verify_code(email, entered_code):
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     cursor.execute("""
#         SELECT verification_code, expires_at FROM email_verifications WHERE e_mail_address = %s
#     """, (email,))
    
#     result = cursor.fetchone()
    
#     if result:
        
#         saved_code, expires_at = result
        
#         if datetime.datetime.now() > expires_at:
#             return "인증 코드가 만료되었습니다."
        
#         if saved_code == entered_code:
#             cursor.execute("UPDATE users SET verification = TRUE WHERE e_mail_address = %s", (email,))
#             connection.commit()
#             cursor.close()
#             connection.close()
#             return "이메일 인증이 성공적으로 완료되었습니다."
        
#         else:
#             return "잘못된 인증 코드입니다."
        
#     else:
#         return "이메일 주소를 찾을 수 없습니다."


def verify_code(email, entered_code):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT verification_code, expires_at FROM email_verifications WHERE e_mail_address = %s
    """, (email,))
    
    result = cursor.fetchone()
    cursor.close()
    connection.close()

    if result:
        saved_code, expires_at = result['verification_code'], result['expires_at']
        
        if expires_at is None:
            return "인증 코드의 만료 시간을 확인할 수 없습니다."
        
        # datetime 형식이 맞는지 확인
        if not isinstance(expires_at, datetime.datetime):
            try:
                expires_at = datetime.datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return "인증 코드의 만료 시간이 잘못되었습니다."
        
        if datetime.datetime.now() > expires_at:
            return "인증 코드가 만료되었습니다."
        
        if saved_code == entered_code:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (e_mail_address, verification) 
                VALUES (%s, TRUE)
                ON DUPLICATE KEY UPDATE verification = TRUE
            """, (email,))
            connection.commit()
            cursor.close()
            connection.close()
            return "이메일 인증, 등록이 성공적으로 완료되었습니다."
        else:
            return "잘못된 인증 코드입니다."
    else:
        return "이메일 주소를 찾을 수 없습니다."

#로그기록
# def is_user_verified(email):
#     connection = get_db_connection()
#     cursor = connection.cursor()

#     cursor.execute("SELECT verification FROM users WHERE e_mail_address = %s", (email,))
#     result = cursor.fetchone()
    
#     cursor.close()
#     connection.close()
    
#     if result and result[0]:  # verification이 True이면 인증된 사용자
#         return True
#     return False


def is_user_verified(email):
    try:
        connection = get_db_connection()
        if connection is None:
            raise Exception("Failed to connect to the database.")
        
        cursor = connection.cursor()
        cursor.execute("SELECT verification FROM users WHERE e_mail_address = %s", (email,))
        result = cursor.fetchone()
        
        cursor.close()
        connection.close()
        
        if result and result['verification']:  # verification이 True이면 인증된 사용자
            return True
        return False
    except pymysql.MySQLError as e:
        logger.error(f"MySQL error: {e}")
        st.error(f"Database query failed: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        st.error(f"An unexpected error occurred: {e}")
        return False


def log_user_change(action, email):
    connection = get_db_connection()
    if connection is None:
        return 'Failed to connect to the database.'
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO user_changes (action, e_mail_address, change_time) VALUES (%s, %s, NOW())",
                (action, email)
            )
            connection.commit()
            logger.info(f"Logged user change: {action} - {email}")
    except Exception as e:
        logger.error(f"Failed to log user change: {e}")
    finally:
        if connection is not None:
            connection.close()
