import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_languages():
    result = []
    with psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT language_id, language_name, iso_code FROM oee.language ORDER BY language_name")
            rows = cursor.fetchall()
            for row in rows:
                result.append({
                    "language_id": row[0],
                    "language_name": row[1],
                    "iso_code": row[2]
                })
    return result