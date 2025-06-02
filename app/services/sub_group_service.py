import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_sub_group_data(product_group=None, sub_group=None):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    base_query = """
        SELECT 
            product_group, 
            sub_group, 
            ROUND((avg_completion_time - (0.05 * avg_completion_time)), 2) AS min_completion_time,
            ROUND((avg_completion_time + (0.05 * avg_completion_time)), 2) AS max_completion_time
        FROM oee.completion_time
    """

    conditions = []
    params = []

    if product_group:
        conditions.append("product_group = %s")
        params.append(product_group)
    if sub_group:
        conditions.append("sub_group = %s")
        params.append(sub_group)

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(base_query, tuple(params))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    result = []
    for row in rows:
        result.append({
            "product_group": row[0],
            "sub_group": row[1],
            "min_completion_time": float(row[2]),
            "max_completion_time": float(row[3]),
        })

    return result
