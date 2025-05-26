from fastapi import APIRouter, Query
from typing import Optional, List
from pydantic import BaseModel
from app.services.role_service import get_roles

router = APIRouter()

class RoleOut(BaseModel):
    id: int
    role: str
    can_read: str
    can_write: str
    can_delete: str

@router.get("/roles", response_model=List[RoleOut])
def read_roles(id: Optional[int] = Query(None, description="Optional role ID to filter")):
    return get_roles(role_id=id)
