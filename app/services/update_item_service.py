import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def update_item(item_id, name=None, loc_id=None):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    # Check if item exists
    cursor.execute("SELECT 1 FROM oee.items WHERE item_id = %s", (item_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        return {"error": f"Item with ID '{item_id}' not found."}

    # Build update query dynamically based on provided fields
    updates = []
    params = []
    if name is not None:
        updates.append("name = %s")
        params.append(name)
    if loc_id is not None:
        updates.append("loc_id = %s")
        params.append(loc_id)

    if updates:
        params.append(item_id)
        query = f"UPDATE items SET {', '.join(updates)} WHERE item_id = %s"
        cursor.execute(query, tuple(params))
        connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Item updated successfully",
        "item_id": item_id,
        "updated_fields": { "name": name, "loc_id": loc_id }
    }
