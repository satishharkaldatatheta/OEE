import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def register_location(loc_id, loc_name, address, country):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    # Check if location already exists
    cursor.execute("SELECT 1 FROM oee.location WHERE loc_id = %s", (loc_id,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        return {
            "message": f"Location with ID '{loc_id}' already exists."
        }

    # Insert location
    cursor.execute(
        "INSERT INTO oee.location (loc_id, loc_name, address, country) VALUES (%s, %s, %s, %s)",
        (loc_id, loc_name, address, country)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Location registered successfully",
        "loc_id": loc_id,
        "loc_name": loc_name,
        "address": address,
        "country": country
    }
