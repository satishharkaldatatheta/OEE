from fastapi import APIRouter, HTTPException
from ..services import delete_user_service

router = APIRouter()

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    success = delete_user_service.delete_user(user_id)
    if success:
        return {"message": f"User deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="User not found or could not be deleted")
