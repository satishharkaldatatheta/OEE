import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_user_from_db(username: str):
    query = """
    SELECT 
        id, firstname, lastname, email, username, password,
        status, designation_id, role_id, created_dt
    FROM oee.loginuser 
    WHERE username = %s;
    """
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()
        return user
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
