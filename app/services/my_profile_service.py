import psycopg2
import os

def update_user_profile(
    user_id: int,
    firstname: str = None,
    lastname: str = None,
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

        fields = []
        values = []

        if firstname is not None:
            fields.append("firstname = %s")
            values.append(firstname)
        if lastname is not None:
            fields.append("lastname = %s")
            values.append(lastname)
        if address is not None:
            fields.append("address = %s")
            values.append(address)
        if phone_number is not None:
            fields.append("phone_number = %s")
            values.append(phone_number)
        if postal_code is not None:
            fields.append("postal_code = %s")
            values.append(postal_code)
        if profile_picture_url is not None:
            fields.append("profile_picture_url = %s")
            values.append(profile_picture_url)
        if country_id is not None:
            fields.append("country_id = %s")
            values.append(country_id)
        if language_id is not None:
            fields.append("language_id = %s")
            values.append(language_id)
        if timezone_id is not None:
            fields.append("timezone_id = %s")
            values.append(timezone_id)

        if not fields:
            raise Exception("No fields to update")

        update_query = f"""
            UPDATE oee.loginuser
            SET {', '.join(fields)}
            WHERE id = %s
        """
        values.append(user_id)

        cursor.execute(update_query, tuple(values))

        if cursor.rowcount == 0:
            raise Exception("User not found")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        raise Exception(f"Database error: {e}")


def get_current_profile_picture_url(user_id: int) -> str:
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT profile_picture_url FROM oee.loginuser WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result[0] if result and result[0] else None

    except Exception as e:
        raise Exception(f"Failed to fetch profile picture URL: {e}")
