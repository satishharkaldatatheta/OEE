import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def save_enquiry_data(email_to, subject, email_address, company_name, contact_number, description, attachment):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        query = """
            INSERT INTO oee.enquiry (email_to, subject, email_address, company_name, contact_number, description, attachment)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(query, (
            email_to, subject, email_address, company_name,
            contact_number, description, attachment
        ))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise Exception(f"Database error: {e}")
