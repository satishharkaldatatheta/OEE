from fastapi import APIRouter, HTTPException, Form
from datetime import datetime
import psycopg2, os
from dotenv import load_dotenv
import hashlib

router = APIRouter()
load_dotenv()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/reset-password")
async def reset_password(token: str = Form(...), new_password: str = Form(...)):
    conn = None
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        cursor.execute("""
            SELECT user_id, expires_at FROM oee.password_resets
            WHERE token = %s
        """, (token,))
        result = cursor.fetchone()

        if not result:
            raise HTTPException(status_code=400, detail="Invalid token")

        user_id, expires_at = result
        if expires_at < datetime.utcnow():
            raise HTTPException(status_code=400, detail="Token expired")

        hashed_pw = hash_password(new_password)

        cursor.execute("""
            UPDATE oee.loginuser SET password = %s, status = 'Enabled' WHERE id = %s
        """, (hashed_pw, user_id))

        cursor.execute("""
            DELETE FROM oee.password_resets WHERE user_id = %s
        """, (user_id,))

        conn.commit()
        return {"message": "Password reset successful. Your account is now enabled."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    finally:
        if conn:
            conn.close()