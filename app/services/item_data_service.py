from sqlalchemy import create_engine, text
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# DB setup
engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

def get_item_data(item_id: str):
    query = """
        WITH MeanActiveTime AS (
        SELECT 
            productgroup, 
            item_id, 
            ROUND(AVG(activehours)) AS mean_active
        FROM 
            oee.reactor_oee
        GROUP BY 
            productgroup, item_id
    ),
    oee_calc AS (
        SELECT 
            rd.productgroup, 
            rd.item_id, 
            rd.starttime, 
            rd.endtime, 
            rd.activehours,
            ROUND((
                (rd.activehours / 
                    CASE 
                        WHEN rd.productgroup = 'A' THEN 30 
                        WHEN rd.productgroup IN ('B', 'C') THEN 24 
                        ELSE NULL 
                    END
                ) * 0.98 * 0.98
            )::numeric, 2) AS oee,
            i.loc_id
        FROM 
            oee.reactor_oee rd
        JOIN 
            oee.items i ON rd.item_id = i.item_id
        JOIN 
            MeanActiveTime m ON rd.productgroup = m.productgroup AND rd.item_id = m.item_id
        WHERE 
            rd.activehours BETWEEN m.mean_active * 0.18 AND m.mean_active * 0.85
            AND rd.item_id = :item_id
    )
    SELECT *
    FROM oee_calc
    """
    with engine.connect() as connection:
        result = connection.execute(text(query), {"item_id": item_id})
        columns = result.keys()
        raw_data = [dict(zip(columns, row)) for row in result]

    enriched_data = []
    for row in raw_data:
        start = row["starttime"]
        if isinstance(start, str):
            start = datetime.fromisoformat(start)

        row["week"] = f"{start.isocalendar().week:02d} Week, {start.year}"
        row["month"] = start.strftime("%B")
        row["monthno"] = f"{start.month:02d}{start.year}"

        hour = start.hour
        if 6 <= hour <= 13:
            row["shift"] = 1
        elif 14 <= hour <= 21:
            row["shift"] = 2
        else:
            row["shift"] = 3

        enriched_data.append(row)

    return enriched_data
