import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_current_status(item_id=None):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    base_query = """
        WITH ranked_data AS (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY item_id 
                       ORDER BY start_time DESC NULLS LAST, last_batch_end_time DESC
                   ) AS rn
            FROM oee.reactor_start
            WHERE lapse_time IS NOT NULL
        )
        SELECT 
            CASE 
                WHEN start_time IS NULL THEN NULL 
                ELSE product_group 
            END AS product_group,
            item_id,
            start_time,
            last_batch_end_time,
            lapse_time,
            CASE 
                WHEN start_time IS NULL THEN 'InActive' 
                ELSE 'Active'
            END AS status
        FROM ranked_data
        WHERE rn = 1
    """

    params = []
    if item_id:
        base_query = base_query.replace(
            "WHERE lapse_time IS NOT NULL",
            "WHERE lapse_time IS NOT NULL AND item_id = %s"
        )
        params.append(item_id)

    cursor.execute(base_query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()

    result = []
    for row in rows:
        result.append({
            "product_group": row[0],
            "item_id": row[1],
            "start_time": row[2],
            "last_batch_end_time": row[3],
            "lapse_time": str(row[4]),  # timedelta to string
            "status": row[5]
        })

    return result
