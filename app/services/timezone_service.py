import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_timezones(timezone_id=None):
    result = []
    query = "SELECT timezone_id, timezone_name, utc_offset FROM oee.timezone"
    params = []

    if timezone_id is not None:
        query += " WHERE timezone_id = %s"
        params.append(timezone_id)

    query += " ORDER BY timezone_name"

    with psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            for row in rows:
                result.append({
                    "timezone_id": row[0],
                    "timezone_name": row[1],
                    "utc_offset": row[2]
                })

    return result
