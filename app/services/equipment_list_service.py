import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_equipment_list():
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id AS equipment_id, name AS equipment_name
        FROM oee.equipment
        ORDER BY id
    """)
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {"equipment_id": eq_id, "equipment_name": eq_name}
        for eq_id, eq_name in rows
    ]
