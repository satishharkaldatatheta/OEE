from fastapi import APIRouter, Form
from app.services.location_reg_service import register_location

router = APIRouter()

@router.post("/locations/register")
def register_location_api(
    loc_id: str = Form(..., description="Location ID (primary key)"),
    loc_name: str = Form(..., description="Location name"),
    address: str = Form(..., description="Address"),
    country: str = Form(..., description="Country")
):
    return register_location(loc_id=loc_id, loc_name=loc_name, address=address, country=country)
