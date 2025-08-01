import os, smtplib, uuid
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2

load_dotenv()
RESET_LINK_BASE = "http://vortex.datatheta.com:3000/reset-password"

def send_reset_email(to_email: str, added_by: str, token: str):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    link = f"{RESET_LINK_BASE}/{token}"

    subject = "Welcome to Vortex - Set your password"
    body = f"""
Hello,

You have been added by {added_by} to the Vortex system.

Please click the link below to set your password and activate your account:
{link}

This link is valid for 24 hours.

Regards,  
Vortex Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


def register_user(firstname, lastname, email, username,
                  designation_id, role_id, location_ids, item_ids, added_by):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        status = "Disabled"

        cursor.execute("""
            INSERT INTO oee.loginuser 
            (firstname, lastname, email, username, designation_id, role_id, status, added_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            firstname, lastname, email, username,
            designation_id, role_id, status, added_by
        ))
        user_id = cursor.fetchone()[0]

        for loc_id in location_ids:
            loc_id = loc_id.strip()
            if loc_id:
                cursor.execute("INSERT INTO oee.userlocations (user_id, loc_id) VALUES (%s, %s)", (user_id, loc_id))

        for item_id in item_ids:
            item_id = item_id.strip()
            if item_id:
                cursor.execute("INSERT INTO oee.useritems (user_id, item_id) VALUES (%s, %s)", (user_id, item_id))

        token = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(hours=24)

        cursor.execute("""
            INSERT INTO oee.password_resets (user_id, token, expires_at)
            VALUES (%s, %s, %s)
        """, (user_id, token, expires_at))

        cursor.execute("SELECT firstname, lastname FROM oee.loginuser WHERE id = %s", (added_by,))
        adder = cursor.fetchone()
        added_by_name = f"{adder[0]} {adder[1]}" if adder else "an admin"

        send_reset_email(email, added_by_name, token)

        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise Exception(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
