import psycopg2
import os
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def update_user_profile(user_id: int, firstname: str, lastname: str, password: str):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        hashed_pw = hash_password(password)

        update_query = """
            UPDATE oee.loginuser
            SET firstname = %s,
                lastname = %s,
                password = %s,
                modified_dt = NOW()
            WHERE id = %s
        """
        cursor.execute(update_query, (firstname, lastname, hashed_pw, user_id))

        if cursor.rowcount == 0:
            raise Exception("User not found")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        raise Exception(f"Database error: {e}")
