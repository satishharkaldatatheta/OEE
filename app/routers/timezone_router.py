from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.timezone_service import get_timezones

router = APIRouter()

class TimezoneOut(BaseModel):
    timezone_id: int
    timezone_name: str
    utc_offset: str

@router.get("/timezones")
def read_timezones():
    """
    Retrieve the list of all timezones.
    """
    return get_timezones()