from fastapi import APIRouter, Form
from app.services.item_service import register_item

router = APIRouter()

@router.post("/items/register")
def register_equipment_item(
    item_id: str = Form(..., description="Unique Item ID (string)"),
    item_name: str = Form(..., description="Name of the item"),
    equipment_id: str = Form(..., description="Equipment ID (string)"),
    loc_id: str = Form(..., description="Location ID")
):
    return register_item(item_id=item_id, item_name=item_name, equipment_id=equipment_id, loc_id=loc_id)
