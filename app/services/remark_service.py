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

def insert_multiple_remarks(user_id: int, remark_ids: list, remark_category_ids: list,
                            item_id: str, loc_id: str, status: str, oee: float):
    query = """
    INSERT INTO oee.remarks 
    (user_id, remark_id, remark_category_id, item_id, loc_id, status, oee)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    conn = get_db_connection()
    inserted_ids = []
    try:
        with conn:
            with conn.cursor() as cur:
                for remark_id, remark_category_id in zip(remark_ids, remark_category_ids):
                    cur.execute(query, (
                        user_id,
                        remark_id,
                        remark_category_id,
                        item_id,
                        loc_id,
                        status,
                        oee
                    ))
                    inserted_ids.append(cur.fetchone()[0])
        return inserted_ids
    finally:
        conn.close()
