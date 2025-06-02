import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_equipment_data(loc_id=None, item_id=None, user_id=None):
    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )
    cursor = connection.cursor()

    # 1. Fetch all equipment
    cursor.execute("""
        SELECT id AS equipment_id, name AS equipment_name
        FROM oee.equipment
        ORDER BY id
    """)
    equipment_rows = cursor.fetchall()

    equipment_map = {
        eq_id: {
            "equipment_id": eq_id,
            "equipment_name": eq_name,
            "items": []
        }
        for eq_id, eq_name in equipment_rows
    }

    # 2. Fetch items filtered by user_id, loc_id, item_id
    base_items_query = """
        SELECT i.item_id, i.name AS item_name,
               i.equipment_id,
               l.loc_id, l.loc_name AS location_name,
               t.name AS team_name
        FROM oee.items i
        LEFT JOIN oee.location l ON i.loc_id = l.loc_id
        LEFT JOIN oee.team t ON i.team_id = t.team_id
    """

    # Add join with useritems if filtering by user
    if user_id:
        base_items_query += """
        INNER JOIN oee.useritems ui ON i.item_id = ui.item_id
        WHERE ui.user_id = %s
        """
        params = [user_id]
    else:
        base_items_query += " WHERE 1=1"
        params = []

    if loc_id:
        base_items_query += " AND l.loc_id = %s"
        params.append(loc_id)

    if item_id:
        base_items_query += " AND i.item_id = %s"
        params.append(item_id)

    cursor.execute(base_items_query, tuple(params))
    item_rows = cursor.fetchall()

    for item_id_val, item_name, equipment_id, loc_id_val, location_name, team_name in item_rows:
        if equipment_id in equipment_map:
            equipment_map[equipment_id]["items"].append({
                "item_id": item_id_val,
                "item_name": item_name,
                "loc_id": loc_id_val,
                "location_name": location_name,
                "team_name": team_name
            })

    cursor.close()
    connection.close()

    return list(equipment_map.values())
