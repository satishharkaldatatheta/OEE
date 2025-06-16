from fastapi import APIRouter
from app.services.equipment_list_service import get_equipment_list

router = APIRouter()

@router.get("/equipment_list", summary="Get all equipment")
def equipment_list():
    return get_equipment_list()
