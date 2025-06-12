# remark_comment_service.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import HTTPException
from typing import Optional, List, Dict

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def fetch_grouped_remark_comments(
    remark_category_id: Optional[int] = None,
    remark_id: Optional[int] = None
) -> List[Dict]:
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        query = """
        SELECT 
            rc.id AS remark_category_id,
            rc.category AS remark_category,
            r.id AS remark_id,
            r.remark
        FROM oee.remarks_comment r
        LEFT JOIN oee.remark_category rc ON r.remark_category_id = rc.id
        WHERE 1=1
        """
        params = []

        if remark_category_id:
            query += " AND rc.id = %s"
            params.append(remark_category_id)

        if remark_id:
            query += " AND r.id = %s"
            params.append(remark_id)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        # Grouping logic
        grouped_data = {}
        for row in rows:
            cat_id = row['remark_category_id']
            if cat_id not in grouped_data:
                grouped_data[cat_id] = {
                    "remark_category_id": cat_id,
                    "remark_category": row['remark_category'],
                    "remarks": []
                }
            grouped_data[cat_id]["remarks"].append({
                "remark_id": row["remark_id"],
                "remark": row["remark"]
            })

        return list(grouped_data.values())

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
