from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import hashlib
from app.services.change_password_service import get_user_by_id, update_user_password

router = APIRouter()

class ChangePasswordRequest(BaseModel):
    user_id: int
    current_password: str
    new_password: str

@router.post("/change-password")
async def change_password(request: ChangePasswordRequest):
    user_data = get_user_by_id(request.user_id)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    db_password = user_data[5]
    hashed_current = hashlib.sha256(request.current_password.encode()).hexdigest()

    if db_password != hashed_current:
        raise HTTPException(status_code=401, detail="Incorrect current password")

    hashed_new = hashlib.sha256(request.new_password.encode()).hexdigest()
    update_success = update_user_password(request.user_id, hashed_new)

    if not update_success:
        raise HTTPException(status_code=500, detail="Failed to update password")

    return {"message": "Password changed successfully"}
