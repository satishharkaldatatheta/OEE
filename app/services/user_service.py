import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_users(user_id=None):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()

    query = """
        SELECT u.id, u.firstname, u.lastname, u.email, u.status, u.created_dt,
               d.designation, r.role, u.designation_id, u.role_id
        FROM oee.loginuser u
        LEFT JOIN oee.designation d ON u.designation_id = d.id
        LEFT JOIN oee.roletype r ON u.role_id = r.id
    """
    params = []

    if user_id:
        query += " WHERE u.id = %s"
        params.append(user_id)

    cursor.execute(query, params)
    users = cursor.fetchall()

    results = []

    for user in users:
        uid, firstname, lastname, email, status, created_dt, designation, role, designation_id, role_id = user

        cursor.execute("SELECT item_id FROM oee.useritems WHERE user_id = %s", (uid,))
        item_ids = [row[0] for row in cursor.fetchall()]
        items = "|".join(item_ids)

        cursor.execute("SELECT loc_id FROM oee.userlocations WHERE user_id = %s", (uid,))
        loc_ids = [row[0] for row in cursor.fetchall()]
        locations = "|".join(loc_ids)

        results.append({
            "user_id": uid,
            "name": f"{firstname} {lastname}",
            "email": email,
            "role": role,
            "role_id": role_id,
            "designation": designation,
            "designation_id": designation_id,
            "createdate": created_dt.strftime("%Y-%m-%d %H:%M:%S"),
            "items": items,
            "locations": locations,
            "status": status
        })

    cursor.close()
    conn.close()
    return results[0] if user_id and results else results



def toggle_user_status(user_id):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = conn.cursor()

    # Fetch current status
    cursor.execute("SELECT status FROM oee.loginuser WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if not result:
        return None

    current_status = result[0]
    new_status = "Disabled" if current_status == "Enabled" else "Enabled"

    cursor.execute("UPDATE oee.loginuser SET status = %s WHERE id = %s", (new_status, user_id))
    conn.commit()

    cursor.close()
    conn.close()
    return new_status
