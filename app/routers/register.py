from fastapi import APIRouter, Form, HTTPException
from ..services.register_service import register_user

router = APIRouter()

@router.post("/register")
async def register(
    firstname: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    designation_id: int = Form(...),
    role_id: int = Form(...),
    location_ids: list[str] = Form(...), 
    item_ids: list[str] = Form(...),
    added_by: int = Form(...)
):
    try:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if len(location_ids) == 1 and "," in location_ids[0]:
            location_ids = location_ids[0].split(",")
        if len(item_ids) == 1 and "," in item_ids[0]:
            item_ids = item_ids[0].split(",")

        register_user(
            firstname, lastname, email, username, password,
            designation_id, role_id, location_ids, item_ids, added_by
        )
        return {"message": "User registered successfully. Status is set to Disabled. An email has been sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))