from fastapi import APIRouter, Query
from typing import Optional
from app.services.sub_group_service import get_sub_group_data

router = APIRouter()

@router.get("/sub_group")
def sub_group(
    product_group: Optional[str] = Query(None, description="Filter by product group"),
    sub_group: Optional[str] = Query(None, description="Filter by sub group")
):
    return get_sub_group_data(product_group=product_group, sub_group=sub_group)
