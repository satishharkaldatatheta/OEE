from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import psycopg2
import os

router = APIRouter()

# Pydantic models
class DataEntry(BaseModel):
    time: str
    devstatus: str

class DeviceEntry(BaseModel):
    deviceId: str
    type: str
    data: List[DataEntry]

class Payload(BaseModel):
    dataset: List[DeviceEntry] = Field(..., alias="_dataset")

    class Config:
        validate_by_name = True
        populate_by_name = True

# API route
@router.post("/jsontotable")
def insert_json_to_table(payload: Payload):
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        cursor = conn.cursor()

        for device in payload.dataset:
            for entry in device.data:
                try:
                    # Convert Unix time (seconds) to timestamp
                    timestamp = datetime.fromtimestamp(int(entry.time))
                except Exception:
                    raise HTTPException(status_code=400, detail=f"Invalid time format: {entry.time}")

                insert_query = """
                    INSERT INTO oee.tagdata (deviceId, type, time, devstatus)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (device.deviceId, device.type, timestamp, entry.devstatus))

        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Data inserted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
