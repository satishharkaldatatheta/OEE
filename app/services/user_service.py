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
        SELECT 
            u.id, u.firstname, u.lastname, u.email, u.status, u.created_dt,
            d.designation, r.role, u.designation_id, u.role_id,
            u.country_id, c.country_name,
            u.language_id, l.language_name, l.iso_code,
            u.timezone_id, t.timezone_name, t.utc_offset,
            u.profile_picture_url
        FROM oee.loginuser u
        LEFT JOIN oee.designation d ON u.designation_id = d.id
        LEFT JOIN oee.roletype r ON u.role_id = r.id
        LEFT JOIN oee.country c ON u.country_id = c.country_id
        LEFT JOIN oee.language l ON u.language_id = l.language_id
        LEFT JOIN oee.timezone t ON u.timezone_id = t.timezone_id
    """
    params = []

    if user_id:
        query += " WHERE u.id = %s"
        params.append(user_id)

    cursor.execute(query, params)
    users = cursor.fetchall()

    results = []

    for user in users:
        (
            uid, firstname, lastname, email, status, created_dt,
            designation, role, designation_id, role_id,
            country_id, country_name,
            language_id, language_name, iso_code,
            timezone_id, timezone_name, utc_offset,
            profile_picture_url
        ) = user

        # Get user items
        cursor.execute("SELECT item_id FROM oee.useritems WHERE user_id = %s", (uid,))
        item_ids = [row[0] for row in cursor.fetchall()]
        items = "|".join(str(i) for i in item_ids)

        # Get user locations
        cursor.execute("SELECT loc_id FROM oee.userlocations WHERE user_id = %s", (uid,))
        loc_ids = [row[0] for row in cursor.fetchall()]
        locations = "|".join(str(l) for l in loc_ids)

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
            "status": status,
            "country_id": country_id,
            "country_name": country_name,
            "language_id": language_id,
            "language_name": language_name,
            "iso_code": iso_code,
            "timezone_id": timezone_id,
            "timezone_name": timezone_name,
            "utc_offset": utc_offset,
            "profile_picture_url": profile_picture_url
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
