import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def register_equipment(id, name):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    # Check if equipment ID already exists
    cursor.execute("SELECT 1 FROM oee.equipment WHERE id = %s", (id,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return {
            "message": f"Equipment with ID '{id}' already exists."
        }

    # Insert new equipment
    cursor.execute(
        "INSERT INTO oee.equipment (id, name) VALUES (%s, %s)",
        (id, name)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Equipment registered successfully",
        "equipment_id": id,
        "equipment_name": name
    }
