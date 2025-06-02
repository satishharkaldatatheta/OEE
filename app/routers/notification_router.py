from fastapi import APIRouter, Query
from typing import Optional
from app.services.notification_service import (
    calculate_and_insert_notifications,
    get_notifications_for_user,
    mark_notifications_as_read
)

router = APIRouter()

@router.post("/notifications/generate")
def generate_notifications():
    return calculate_and_insert_notifications()

@router.get("/notifications")
def fetch_user_notifications(
    user_id: str = Query(..., description="User ID"),
    read: Optional[bool] = Query(None, description="Filter by read/unread status")
):
    return get_notifications_for_user(user_id=user_id, read=read)

@router.post("/notifications/mark-read")
def mark_user_notifications_read(
    user_id: str = Query(..., description="User ID")
):
    return mark_notifications_as_read(user_id=user_id)
