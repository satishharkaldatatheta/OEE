import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_designations(designation_id=None):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    if designation_id:
        query = "SELECT id, designation FROM oee.designation WHERE id = %s"
        cursor.execute(query, (designation_id,))
    else:
        query = "SELECT id, designation FROM oee.designation"
        cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    result = [{"id": row[0], "designation": row[1]} for row in rows]
    return result
