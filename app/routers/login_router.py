from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.login_service import get_user_from_db
import hashlib

router = APIRouter()

class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: str
    username: str
    status: str
    designation_id: int
    role_id: int
    created_dt: str

@router.post("/login", response_model=User)
async def login(username: str, password: str):
    user_data = get_user_from_db(username)

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    db_password = user_data[5]

    hashed_input = hashlib.sha256(password.encode()).hexdigest()
    if db_password != hashed_input:
        raise HTTPException(status_code=401, detail="Incorrect password")

    user = User(
        id=user_data[0],
        firstname=user_data[1],
        lastname=user_data[2],
        email=user_data[3],
        username=user_data[4],
        status=user_data[6],
        designation_id=user_data[7],
        role_id=user_data[8],
        created_dt=str(user_data[9])
    )
    return user
