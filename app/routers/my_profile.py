from fastapi import APIRouter, Form, HTTPException
from app.services.my_profile_service import update_user_profile

router = APIRouter()

@router.post("/my_profile")
async def my_profile(
    user_id: int = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    try:
        update_user_profile(user_id, firstname, lastname, password)
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
