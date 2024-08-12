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

    
            
def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None