from fastapi import APIRouter, HTTPException, Form
from typing import Optional, List
from app.services import update_user_service

router = APIRouter()

@router.put("/update_user/{user_id}")
def update_user(
    user_id: int,
    firstname: Optional[str] = Form(None),
    lastname: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    designation_id: Optional[int] = Form(None),
    role_id: Optional[int] = Form(None),
    location_ids: List[str] = Form([]),  # multiple form fields or single CSV string
    item_ids: List[str] = Form([]),
):
    # Normalize item_ids if passed as single CSV string
    if len(item_ids) == 1 and "," in item_ids[0]:
        item_ids = [x.strip() for x in item_ids[0].split(",") if x.strip()]

    # Normalize location_ids if passed as single CSV string
    if len(location_ids) == 1 and "," in location_ids[0]:
        location_ids = [x.strip() for x in location_ids[0].split(",") if x.strip()]

    update_data = {}

    if firstname is not None:
        update_data["firstname"] = firstname
    if lastname is not None:
        update_data["lastname"] = lastname
    if email is not None:
        update_data["email"] = email
    if designation_id is not None:
        update_data["designation_id"] = designation_id
    if role_id is not None:
        update_data["role_id"] = role_id
    if location_ids:
        update_data["locations"] = location_ids
    if item_ids:
        update_data["items"] = item_ids

    success = update_user_service.update_user(user_id, update_data)

    if not success:
        raise HTTPException(status_code=404, detail="User not found or update failed")

    return {"message": "User updated successfully", "user_id": user_id}
