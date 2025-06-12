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

def insert_remark(user_id: int, remark_id: int, remark_category_id: int,
                  item_id: str, loc_id: str, status: str, oee: float,
                  problem: str):
    query = """
    INSERT INTO oee.remarks 
    (user_id, remark_id, remark_category_id, item_id, loc_id, status, oee, problem)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    conn = get_db_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(query, (
                    user_id,
                    remark_id,
                    remark_category_id,
                    item_id,
                    loc_id,
                    status,
                    oee,
                    problem
                ))
                inserted_id = cur.fetchone()[0]
        return inserted_id
    finally:
        conn.close()