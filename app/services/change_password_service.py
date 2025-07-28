import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_user_by_id(user_id: int):
    query = """
    SELECT 
        id, firstname, lastname, email, username, password,
        status, designation_id, role_id, created_dt, modified_dt,
        address, phone_number, postal_code, profile_picture_url
    FROM oee.loginuser 
    WHERE id = %s;
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        with conn.cursor() as cursor:
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_user_password(user_id: int, new_hashed_password: str) -> bool:
    query = """
    UPDATE oee.loginuser
    SET password = %s,
        modified_dt = NOW()
    WHERE id = %s;
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        with conn.cursor() as cursor:
            cursor.execute(query, (new_hashed_password, user_id))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        if conn:
            conn.close()
