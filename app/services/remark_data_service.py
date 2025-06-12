import psycopg2
import os
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

def fetch_remark_data(user_id=None, item_id=None, remark_id=None, loc_id=None, remark_category_id=None):
    query = """
    SELECT 
        r.item_id,
        i.name,
        r.status,
        r.remark_id,
        r.remark_category_id,
        rc.remark AS remark,
        CONCAT(lu.firstname, ' ', lu.lastname) AS user_name,
        r.loc_id,
        r.created_dt::date AS date,
        r.created_dt::time AS time
    FROM oee.remarks r
    LEFT JOIN oee.remarks_comment rc ON r.remark_id = rc.id
    LEFT JOIN oee.items i ON r.item_id = i.item_id
    LEFT JOIN oee.loginuser lu ON r.user_id = lu.id
    WHERE 1=1
    """
    params = []

    if user_id is not None:
        query += " AND r.user_id = %s"
        params.append(user_id)
    if item_id is not None:
        query += " AND r.item_id = %s"
        params.append(item_id)
    if remark_id is not None:
        query += " AND r.remark_id = %s"
        params.append(remark_id)
    if loc_id is not None:
        query += " AND r.loc_id = %s"
        params.append(loc_id)
    if remark_category_id is not None:
        query += " AND r.remark_category_id = %s"
        params.append(remark_category_id)

    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                results = [dict(zip(columns, row)) for row in rows]
        return results
    finally:
        conn.close()
