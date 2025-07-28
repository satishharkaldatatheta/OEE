import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_countries():
    result = []
    with psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT country_id, country_name FROM oee.country ORDER BY country_name")
            rows = cursor.fetchall()
            for row in rows:
                result.append({
                    "country_id": row[0],
                    "country_name": row[1]
                })
    return result