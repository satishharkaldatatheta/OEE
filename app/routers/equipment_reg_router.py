from fastapi import APIRouter, Form
from app.services.equipment_reg_service import register_equipment

router = APIRouter()

@router.post("/equipment/register")
def register_equipment_api(
    id: str = Form(..., description="Equipment ID (primary key, string)"),
    name: str = Form(..., description="Equipment name")
):
    return register_equipment(id=id, name=name)
