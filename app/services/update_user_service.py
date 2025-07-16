import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def update_user(user_id, update_data):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT id FROM oee.loginuser WHERE id = %s", (user_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    # Update loginuser fields dynamically
    fields = []
    values = []

    for key in ["firstname", "lastname", "email", "designation_id", "role_id"]:
        if key in update_data:
            fields.append(f"{key} = %s")
            values.append(update_data[key])

    if fields:
        query = f"UPDATE oee.loginuser SET {', '.join(fields)} WHERE id = %s"
        values.append(user_id)
        cursor.execute(query, values)

    # Update useritems if present
    if "items" in update_data:
        # Delete old entries
        cursor.execute("DELETE FROM oee.useritems WHERE user_id = %s", (user_id,))
        # Insert new entries
        for item_id in update_data["items"]:
            cursor.execute(
                "INSERT INTO oee.useritems (user_id, item_id) VALUES (%s, %s)",
                (user_id, item_id)
            )

    # Update userlocations if present
    if "locations" in update_data:
        # Delete old entries
        cursor.execute("DELETE FROM oee.userlocations WHERE user_id = %s", (user_id,))
        # Insert new entries
        for loc_id in update_data["locations"]:
            cursor.execute(
                "INSERT INTO oee.userlocations (user_id, loc_id) VALUES (%s, %s)",
                (user_id, loc_id)
            )

    conn.commit()
    cursor.close()
    conn.close()
    return True