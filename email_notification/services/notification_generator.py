from datetime import datetime, timezone
from .db import get_db_connection

def generate_notifications():
    conn = get_db_connection()
    cur  = conn.cursor()
    now  = datetime.now(timezone.utc)

    cur.execute("""
        SELECT item_id, MAX(endtime) AS latest_endtime
        FROM oee.reactor_data
        GROUP BY item_id
    """)
    rows = cur.fetchall()

    inserted = 0
    for item_id, endtime in rows:
        if not endtime:
            continue
        if endtime.tzinfo is None:
            endtime = endtime.replace(tzinfo=timezone.utc)
        hours = int((now - endtime).total_seconds() // 3600)

        if   hours > 72:
            intensity, desc = "high", "Inactive for more than 72 hours"
        elif hours > 48:
            intensity, desc = "medium", "Inactive for more than 48 hours"
        elif hours > 24:
            intensity, desc = "low", "Inactive for more than 24 hours"
        else:
            continue

        cur.execute("SELECT equipment_id, loc_id FROM oee.items WHERE item_id=%s", (item_id,))
        row = cur.fetchone()
        if not row:
            continue
        equipment_id, loc_id = row

        cur.execute("""
            SELECT 1 FROM oee.notifications
            WHERE item_id=%s AND intensity=%s AND created_at::date=CURRENT_DATE
        """, (item_id, intensity))
        if cur.fetchone():
            continue

        cur.execute("""
            INSERT INTO oee.notifications (
                item_id, equipment_id, loc_id,
                intensity, inactive_since, inactive_hours,
                created_at, read, description
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,FALSE,%s)
            RETURNING id
        """, (item_id, equipment_id, loc_id,
              intensity, endtime, hours, now, desc))
        notif_id = cur.fetchone()[0]
        inserted += 1

        cur.execute("SELECT user_id FROM oee.useritems WHERE item_id=%s", (item_id,))
        for (user_id,) in cur.fetchall():
            cur.execute("""
                INSERT INTO oee.user_notifications (user_id, notification_id, is_read)
                VALUES (%s,%s,FALSE)
                ON CONFLICT DO NOTHING
            """, (user_id, notif_id))

    conn.commit()
    cur.close(); conn.close()
    print(f"{inserted} notifications generated.")
