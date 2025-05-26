import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def delete_item(item_id):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    # Check if item exists
    cursor.execute("SELECT 1 FROM items WHERE oee.item_id = %s", (item_id,))
    if not cursor.fetchone():
        cursor.close()
        connection.close()
        return {"error": f"Item with ID '{item_id}' not found."}

    # Delete the item
    cursor.execute("DELETE FROM oee.items WHERE item_id = %s", (item_id,))
    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Item deleted successfully",
        "item_id": item_id
    }
