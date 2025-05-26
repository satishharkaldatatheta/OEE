from fastapi import APIRouter, Query
from typing import Optional, List
from pydantic import BaseModel
from app.services.designation_service import get_designations

router = APIRouter()

class DesignationOut(BaseModel):
    id: int
    designation: str

@router.get("/designations", response_model=List[DesignationOut])
def read_designations(id: Optional[int] = Query(None, description="Optional designation ID to filter")):
    return get_designations(designation_id=id)
