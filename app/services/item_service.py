import os
import psycopg2
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

def register_item(item_id, item_name, equipment_id, loc_id):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    # Check if item_id already exists
    cursor.execute("SELECT 1 FROM oee.items WHERE item_id = %s", (item_id,))
    if cursor.fetchone():
        cursor.close()
        connection.close()
        raise HTTPException(status_code=400, detail=f"Item with ID '{item_id}' already exists.")

    # Proceed to insert
    insert_query = """
        INSERT INTO oee.items (item_id, name, equipment_id, loc_id)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (item_id, item_name, equipment_id, loc_id))
    connection.commit()
    cursor.close()
    connection.close()

    return {
        "message": "Item registered successfully",
        "item_id": item_id,
        "item_name": item_name,
        "equipment_id": equipment_id,
        "loc_id": loc_id
    }
