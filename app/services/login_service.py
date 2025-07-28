import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

def get_user_from_db(email: str):
    query = """
    SELECT 
        u.id, u.firstname, u.lastname, u.email, u.username, u.password,
        u.status, u.designation_id, u.role_id, u.created_dt, u.modified_dt,
        u.address, u.phone_number, u.postal_code, u.profile_picture_url,
        u.country_id, c.country_name,
        u.timezone_id, t.timezone_name, t.utc_offset,
        u.language_id, l.language_name, l.iso_code
    FROM oee.loginuser u
    LEFT JOIN oee.country c ON u.country_id = c.country_id
    LEFT JOIN oee.timezone t ON u.timezone_id = t.timezone_id
    LEFT JOIN oee.language l ON u.language_id = l.language_id
    WHERE u.email = %s;
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
            cursor.execute(query, (email,))
            user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None
    finally:
        if conn:
            conn.close()
