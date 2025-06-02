from fastapi import APIRouter, Query
from typing import Optional
from app.services.current_status_service import get_current_status

router = APIRouter()

@router.get("/current_status")
def current_status(item_id: Optional[str] = Query(None, description="Filter by item ID")):
    return get_current_status(item_id=item_id)
