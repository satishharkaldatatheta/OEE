from fastapi import APIRouter, Query, status
from typing import Optional
from app.services.notification_service import (
    calculate_and_insert_notifications,
    get_notifications_for_user,
    mark_notifications_as_read
)

router = APIRouter()


@router.post(
    "/notifications/generate",
    summary="Generate notifications based on inactive items",
    status_code=status.HTTP_201_CREATED
)
def generate_notifications():
    return calculate_and_insert_notifications()


@router.get(
    "/notifications",
    summary="Fetch notifications for a user",
    status_code=status.HTTP_200_OK
)
def fetch_user_notifications(
    user_id: str = Query(..., description="User ID"),
    read: Optional[bool] = Query(None, description="Filter by read (true) or unread (false)")
):
    return get_notifications_for_user(user_id=user_id, read=read)


@router.post(
    "/notifications/mark-read",
    summary="Mark one or all notifications as read",
    status_code=status.HTTP_200_OK
)
def mark_user_notifications_read(
    user_id: str = Query(..., description="User ID"),
    notification_id: Optional[int] = Query(
        None,
        description="Notification ID to mark as read. If not provided, all unread will be marked."
    )
):
    return mark_notifications_as_read(user_id=user_id, notification_id=notification_id)
