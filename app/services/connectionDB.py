import psycopg2
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

print({os.getenv("POSTGRES_DB")})

def connect_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()
        print("Connection Successful:{conn}")

    except Exception as e:
        raise Exception(f"Database error: {e}")
    
connect_db()