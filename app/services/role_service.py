import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_roles(role_id=None):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    if role_id:
        query = """
            SELECT id, role, can_read, can_write, can_delete
            FROM oee.roletype
            WHERE id = %s and id!=1
        """
        cursor.execute(query, (role_id,))
    else:
        query = """
            SELECT id, role, can_read, can_write, can_delete
            FROM oee.roletype where id!=1
        """
        cursor.execute(query)

    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "role": row[1],
            "can_read": row[2],
            "can_write": row[3],
            "can_delete": row[4]
        })

    return result
