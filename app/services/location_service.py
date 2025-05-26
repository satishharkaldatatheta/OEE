import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Function to get a database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

def get_all_locations():
    query = "SELECT loc_id, loc_name, address, country FROM oee.location"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    locations = cursor.fetchall()
    conn.close()
    return locations

def get_location_by_id(loc_id: str):
    query = "SELECT loc_id, loc_name, address, country FROM oee.location WHERE loc_id = %s"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (loc_id,))
    location = cursor.fetchone()
    conn.close()
    return location

def get_locations_by_country(country: str):
    query = "SELECT loc_id, loc_name, address, country FROM oee.location WHERE country = %s"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (country,))
    locations = cursor.fetchall()
    conn.close()
    return locations
