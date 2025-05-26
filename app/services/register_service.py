import psycopg2
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(firstname, lastname, email, username, password,
                  designation_id, role_id, location_ids, item_ids):
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
        status = "Disabled"

        # Insert user
        insert_user_query = """
            INSERT INTO oee.loginuser (firstname, lastname, email, username, password, designation_id, role_id, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(insert_user_query, (
            firstname, lastname, email, username, hashed_pw,
            designation_id, role_id, status
        ))
        user_id = cursor.fetchone()[0]

        # Insert locations
        insert_location_query = """
            INSERT INTO oee.userlocations (user_id, loc_id)
            VALUES (%s, %s)
        """
        for loc_id in location_ids:
            loc_id = loc_id.strip()
            if loc_id:
                cursor.execute(insert_location_query, (user_id, loc_id))

        # Insert items
        insert_item_query = """
            INSERT INTO oee.useritems (user_id, item_id)
            VALUES (%s, %s)
        """
        for item_id in item_ids:
            item_id = item_id.strip()
            if item_id:
                cursor.execute(insert_item_query, (user_id, item_id))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        raise Exception(f"Database error: {e}")
