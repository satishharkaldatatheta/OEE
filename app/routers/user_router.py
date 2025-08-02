from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services import user_service

router = APIRouter()

@router.get("/users")
@router.get("/users/{user_id}")
def get_users(user_id: Optional[int] = None):
    return user_service.get_users(user_id=user_id)

@router.patch("/users/{user_id}/status")
def toggle_user_status(user_id: int):
    updated_status = user_service.toggle_user_status(user_id)
    if updated_status:
        return {"user_id": user_id, "new_status": updated_status}
    raise HTTPException(status_code=404, detail="User not found")