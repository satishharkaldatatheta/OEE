import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def add_bookmark(user_id: int, equipment_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO oee.bookmarks (user_id, equipment_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (user_id, equipment_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Bookmark added"}

def remove_bookmark(user_id: int, equipment_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM oee.bookmarks
        WHERE user_id = %s AND equipment_id = %s
    """, (user_id, equipment_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Bookmark removed"}

def get_user_bookmarks(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT equipment_id
        FROM oee.bookmarks
        WHERE user_id = %s
    """, (user_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in rows]

def is_bookmarked(user_id: int, equipment_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 1
        FROM oee.bookmarks
        WHERE user_id = %s AND equipment_id = %s
        LIMIT 1
    """, (user_id, equipment_id))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return {"bookmarked": exists}
