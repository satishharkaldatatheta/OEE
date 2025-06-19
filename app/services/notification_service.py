from datetime import datetime, timedelta, timezone
import psycopg2
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )


def calculate_and_insert_notifications():
    connection = get_db_connection()
    cursor = connection.cursor()
    now = datetime.now(timezone.utc)

    cursor.execute("""
        SELECT item_id, MAX(endtime) AS latest_endtime
        FROM oee.reactor_data
        GROUP BY item_id
    """)
    reactor_items = cursor.fetchall()

    inserted_count = 0

    for item_id, endtime in reactor_items:
        if endtime is None:
            continue

        # Convert to timezone-aware if it's not already
        if endtime.tzinfo is None:
            endtime = endtime.replace(tzinfo=timezone.utc)

        delta = now - endtime
        hours_inactive = int(delta.total_seconds() // 3600)

        intensity = None
        if hours_inactive > 72:
            intensity = "high"
        elif hours_inactive > 48:
            intensity = "medium"
        elif hours_inactive > 24:
            intensity = "low"

        if not intensity:
            continue

        cursor.execute("""
            SELECT equipment_id, loc_id
            FROM oee.items
            WHERE item_id = %s
        """, (item_id,))
        item_info = cursor.fetchone()
        if not item_info:
            continue

        equipment_id, loc_id = item_info

        cursor.execute("""
            SELECT id FROM oee.notifications
            WHERE item_id = %s AND intensity = %s AND created_at::date = CURRENT_DATE
        """, (item_id, intensity))
        existing = cursor.fetchone()
        if existing:
            continue

        cursor.execute("""
            INSERT INTO oee.notifications (
                item_id, equipment_id, loc_id,
                intensity, inactive_since, inactive_hours,
                created_at, read
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            item_id, equipment_id, loc_id,
            intensity, endtime, hours_inactive,
            now, False
        ))
        notification_id = cursor.fetchone()[0]
        inserted_count += 1

        cursor.execute("SELECT user_id FROM oee.useritems WHERE item_id = %s", (item_id,))
        user_rows = cursor.fetchall()

        for (user_id,) in user_rows:
            cursor.execute("""
                INSERT INTO oee.user_notifications (user_id, notification_id, is_read)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id, notification_id) DO NOTHING
            """, (user_id, notification_id, False))

    connection.commit()
    cursor.close()
    connection.close()
    return {"message": f"{inserted_count} new notifications inserted."}


def get_notifications_for_user(user_id: str, read: Optional[bool] = None):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        SELECT n.id, n.item_id, n.equipment_id, n.loc_id,
               n.intensity, n.inactive_since, n.inactive_hours,
               n.created_at, un.is_read
        FROM oee.user_notifications un
        JOIN oee.notifications n ON un.notification_id = n.id
        WHERE un.user_id = %s
    """
    params = [user_id]

    if read is not None:
        query += " AND un.is_read = %s"
        params.append(read)

    query += " ORDER BY n.created_at DESC"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()

    result = [
        {
            "notification_id": row[0],
            "item_id": row[1],
            "equipment_id": row[2],
            "loc_id": row[3],
            "intensity": row[4],
            "inactive_since": row[5],
            "inactive_hours": row[6],
            "created_at": row[7],
            "is_read": row[8]
        }
        for row in rows
    ]

    cursor.close()
    connection.close()
    return result


def mark_notifications_as_read(user_id: str, notification_id: Optional[int] = None):
    connection = get_db_connection()
    cursor = connection.cursor()

    if notification_id:
        cursor.execute("""
            UPDATE oee.user_notifications
            SET is_read = TRUE
            WHERE user_id = %s AND notification_id = %s AND is_read = FALSE
        """, (user_id, notification_id))
    else:
        cursor.execute("""
            UPDATE oee.user_notifications
            SET is_read = TRUE
            WHERE user_id = %s AND is_read = FALSE
        """, (user_id,))

    updated = cursor.rowcount
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": f"{updated} notification(s) marked as read."}
