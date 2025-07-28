import psycopg2
import os

def update_user_profile(
    user_id: int,
    firstname: str,
    lastname: str,
    address: str = None,
    phone_number: str = None,
    postal_code: str = None,
    profile_picture_url: str = None,
    country_id: int = None,
    language_id: int = None,
    timezone_id: int = None
):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        update_query = """
            UPDATE oee.loginuser
            SET firstname = %s,
                lastname = %s,
                address = %s,
                phone_number = %s,
                postal_code = %s,
                profile_picture_url = %s,
                country_id = %s,
                language_id = %s,
                timezone_id = %s
            WHERE id = %s
        """
        cursor.execute(update_query, (
            firstname,
            lastname,
            address,
            phone_number,
            postal_code,
            profile_picture_url,
            country_id,
            language_id,
            timezone_id,
            user_id
        ))

        if cursor.rowcount == 0:
            raise Exception("User not found")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        raise Exception(f"Database error: {e}")
