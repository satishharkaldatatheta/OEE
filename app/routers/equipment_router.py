from fastapi import APIRouter, Query
from typing import Optional
from app.services.equipment_service import get_equipment_data

router = APIRouter()

@router.get("/equipment")
def get_equipment(
    loc_id: Optional[str] = Query(None, description="Filter by location id"),
    item_id: Optional[str] = Query(None, description="Filter by item id")
):
    return get_equipment_data(loc_id=loc_id, item_id=item_id)
