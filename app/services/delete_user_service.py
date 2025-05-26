import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def delete_user(user_id: int):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        # Delete from useritems
        cursor.execute("DELETE FROM oee.useritems WHERE user_id = %s", (user_id,))

        # Delete from userlocations
        cursor.execute("DELETE FROM oee.userlocations WHERE user_id = %s", (user_id,))

        # Delete from loginuser
        cursor.execute("DELETE FROM oee.loginuser WHERE id = %s", (user_id,))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False
