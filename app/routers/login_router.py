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
    modified_dt: str
    address: str | None = None
    phone_number: str | None = None
    postal_code: str | None = None
    profile_picture_url: str | None = None
    country_id: int | None = None
    country_name: str | None = None
    timezone_id: int | None = None
    timezone_name: str | None = None
    utc_offset: str | None = None
    language_id: int | None = None
    language_name: str | None = None
    iso_code: str | None = None

@router.post("/login", response_model=User)
async def login(email: str, password: str):
    user_data = get_user_from_db(email)

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
        created_dt=str(user_data[9]),
        modified_dt=str(user_data[10]),
        address=user_data[11],
        phone_number=user_data[12],
        postal_code=user_data[13],
        profile_picture_url=user_data[14],
        country_id=user_data[15],
        country_name=user_data[16],
        timezone_id=user_data[17],
        timezone_name=user_data[18],
        utc_offset=user_data[19],
        language_id=user_data[20],
        language_name=user_data[21],
        iso_code=user_data[22]
    )
    return user
