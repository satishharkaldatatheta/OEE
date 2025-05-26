import os
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def get_notifications_from_db(read=None):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT id, item_id, equipment_id, loc_id, intensity, created_at, read
        FROM oee.notifications
    """
    params = []

    if read is not None:
        query += " WHERE read = %s"
        params.append(read)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    notifications = []
    for row in rows:
        notifications.append({
            "id": row[0],
            "item_id": row[1],
            "equipment_id": row[2],
            "loc_id": row[3],
            "intensity": row[4],
            "created_at": row[5],
            "read": row[6]
        })

    cursor.close()
    connection.close()
    return notifications

def mark_notifications_as_read():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE notifications SET read = TRUE WHERE read = FALSE")
    updated_count = cursor.rowcount

    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"{updated_count} notifications marked as read."}

def calculate_and_insert_notifications():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT rd.item_id, MAX(rd.endtime) AS latest_endtime,
               i.equipment_id, i.loc_id
        FROM oee.reactor_data rd
        JOIN oee.items i ON rd.item_id = i.item_id
        GROUP BY rd.item_id, i.equipment_id, i.loc_id
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    now = datetime.now()
    inserted_count = 0

    for item_id, endtime, equipment_id, loc_id in rows:
        if endtime is None:
            continue

        delta = now - endtime

        intensity = None
        if delta > timedelta(hours=72):
            intensity = "high"
        elif delta > timedelta(hours=48):
            intensity = "medium"
        elif delta > timedelta(hours=24):
            intensity = "low"

        if intensity:
            # Avoid duplicate notification for same day and intensity
            check_query = """
                SELECT 1 FROM oee.notifications
                WHERE item_id = %s AND intensity = %s AND DATE(created_at) = CURRENT_DATE
            """
            cursor.execute(check_query, (item_id, intensity))
            if not cursor.fetchone():
                insert_query = """
                    INSERT INTO oee.notifications (item_id, equipment_id, loc_id, intensity)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (item_id, equipment_id, loc_id, intensity))
                inserted_count += 1

    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"{inserted_count} new notifications inserted."}
