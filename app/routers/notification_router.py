from fastapi import APIRouter, Query
from typing import Optional
from app.services.notification_service import (
    get_notifications_from_db,
    mark_notifications_as_read,
    calculate_and_insert_notifications
)

router = APIRouter()

@router.get("/notifications")
def get_notifications(read: Optional[bool] = Query(None, description="Filter by read/unread")):
    return get_notifications_from_db(read)

@router.post("/notifications/mark-read")
def mark_all_notifications_read():
    return mark_notifications_as_read()

@router.post("/notifications/generate")
def generate_notifications():
    return calculate_and_insert_notifications()
