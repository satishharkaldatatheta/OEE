import os
import uuid
import hashlib
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

RESET_URL_BASE = "http://vortex.datatheta.com:3000/reset-password?token="


def create_password_reset_token(email: str) -> bool:
    token = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(minutes=30)

    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute("SELECT id, firstname FROM oee.loginuser WHERE email = %s", (email,))
        user = cursor.fetchone()
        if not user:
            return False

        user_id, firstname = user

        cursor.execute("""
            INSERT INTO oee.password_resets (user_id, token, expires_at)
            VALUES (%s, %s, %s)
        """, (user_id, token, expiry))
        conn.commit()

        send_reset_email(email, firstname, token)
        return True

    except Exception as e:
        print(f"Error generating token: {e}")
        return False

    finally:
        if conn:
            conn.close()


def send_reset_email(to_email: str, firstname: str, token: str):
    link = RESET_URL_BASE + token
    subject = "Reset your password"
    body = f"""\
Hi {firstname},

You requested a password reset. Click the link below to reset it:

{link}

This link is valid for 30 minutes.

If you didn’t request this, you can safely ignore this email.
"""

    msg = EmailMessage()
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


def verify_token_validity(token: str) -> bool:
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM oee.password_resets
            WHERE token = %s AND expires_at > NOW()
        """, (token,))
        return cursor.fetchone() is not None

    except Exception as e:
        print(f"Error verifying token: {e}")
        return False

    finally:
        if conn:
            conn.close()


def update_password_with_token(token: str, new_password: str) -> bool:
    conn = None
    try:
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id FROM oee.password_resets
            WHERE token = %s AND expires_at > NOW()
        """, (token,))
        result = cursor.fetchone()
        if not result:
            return False

        user_id = result[0]
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        cursor.execute("""
            UPDATE oee.loginuser
            SET password = %s, modified_dt = NOW()
            WHERE id = %s
        """, (hashed_password, user_id))

        cursor.execute("DELETE FROM oee.password_resets WHERE token = %s", (token,))
        conn.commit()
        return True

    except Exception as e:
        print(f"Error resetting password: {e}")
        return False

    finally:
        if conn:
            conn.close()
