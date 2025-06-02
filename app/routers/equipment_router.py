from fastapi import APIRouter
from app.services.equipment_service import get_equipment_data
from typing import Optional

router = APIRouter()

@router.get("/equipment")
def get_equipment(
    loc_id: Optional[int] = None,
    item_id: Optional[int] = None,
    user_id: Optional[int] = None
):
    return get_equipment_data(loc_id=loc_id, item_id=item_id, user_id=user_id)
