from datetime import datetime, timezone
import psycopg2
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ────────────────────────────────────────────────────────────────────────────────
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

# ────────────────────────────────────────────────────────────────────────────────
def calculate_and_insert_notifications():
    conn = get_db_connection()
    cur = conn.cursor()
    now = datetime.now(timezone.utc)

    # latest end‑time for each reactor
    cur.execute("""
        SELECT item_id, MAX(endtime) AS latest_endtime
        FROM oee.reactor_data
        GROUP BY item_id
    """)
    rows = cur.fetchall()

    inserted = 0

    for item_id, endtime in rows:
        if endtime is None:
            continue
        if endtime.tzinfo is None:
            endtime = endtime.replace(tzinfo=timezone.utc)

        hours = int((now - endtime).total_seconds() // 3600)

        if   hours > 72:
            intensity   = "high"
            description = "Inactive for more than 72 hours"
        elif hours > 48:
            intensity   = "medium"
            description = "Inactive for more than 48 hours"
        elif hours > 24:
            intensity   = "low"
            description = "Inactive for more than 24 hours"
        else:
            continue  # still active

        # equipment / location
        cur.execute("""
            SELECT equipment_id, loc_id
            FROM oee.items
            WHERE item_id = %s
        """, (item_id,))
        row = cur.fetchone()
        if not row:
            continue
        equipment_id, loc_id = row

        # avoid duplicate notification for today
        cur.execute("""
            SELECT 1 FROM oee.notifications
            WHERE item_id = %s
              AND intensity = %s
              AND created_at::date = CURRENT_DATE
        """, (item_id, intensity))
        if cur.fetchone():
            continue

        # ── insert notification ────────────────────────────────────────────────
        cur.execute("""
            INSERT INTO oee.notifications (
                item_id, equipment_id, loc_id,
                intensity, inactive_since, inactive_hours,
                created_at, read, description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE, %s)
            RETURNING id
        """, (
            item_id, equipment_id, loc_id,
            intensity, endtime, hours, now, description
        ))
        notif_id = cur.fetchone()[0]
        inserted += 1

        # map to every authorised user
        cur.execute("SELECT user_id FROM oee.useritems WHERE item_id = %s", (item_id,))
        for (user_id,) in cur.fetchall():
            cur.execute("""
                INSERT INTO oee.user_notifications (user_id, notification_id, is_read)
                VALUES (%s, %s, FALSE)
                ON CONFLICT DO NOTHING
            """, (user_id, notif_id))

    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"{inserted} new notifications inserted."}

# ────────────────────────────────────────────────────────────────────────────────
def get_notifications_for_user(user_id: str, read: Optional[bool] = None):
    conn = get_db_connection()
    cur  = conn.cursor()

    sql = """
        SELECT n.id, n.item_id, n.equipment_id, n.loc_id, n.intensity,
               n.inactive_since, n.inactive_hours, n.description,
               n.created_at, un.is_read
        FROM   oee.user_notifications un
        JOIN   oee.notifications       n ON un.notification_id = n.id
        WHERE  un.user_id = %s
    """
    params = [user_id]
    if read is not None:
        sql += " AND un.is_read = %s"
        params.append(read)
    sql += " ORDER BY n.created_at DESC"

    cur.execute(sql, tuple(params))
    out = [{
        "notification_id": r[0],
        "item_id":         r[1],
        "equipment_id":    r[2],
        "loc_id":          r[3],
        "intensity":       r[4],
        "inactive_since":  r[5],
        "inactive_hours":  r[6],
        "description":     r[7],
        "created_at":      r[8],
        "is_read":         r[9]
    } for r in cur.fetchall()]

    cur.close(); conn.close()
    return out

# ────────────────────────────────────────────────────────────────────────────────
def mark_notifications_as_read(user_id: str, notification_id: Optional[int] = None):
    conn = get_db_connection()
    cur  = conn.cursor()

    if notification_id:
        cur.execute("""
            UPDATE oee.user_notifications
            SET is_read = TRUE
            WHERE user_id = %s AND notification_id = %s
              AND is_read = FALSE
        """, (user_id, notification_id))
    else:
        cur.execute("""
            UPDATE oee.user_notifications
            SET is_read = TRUE
            WHERE user_id = %s AND is_read = FALSE
        """, (user_id,))

    updated = cur.rowcount
    conn.commit()
    cur.close(); conn.close()
    return {"message": f"{updated} notification(s) marked as read."}
