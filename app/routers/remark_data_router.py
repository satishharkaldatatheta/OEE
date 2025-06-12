from fastapi import APIRouter, Query
from typing import Optional
from app.services.remark_data_service import fetch_remark_data

router = APIRouter()

@router.get("/remark_data")
def get_remark_data(
    user_id: Optional[int] = Query(None),
    item_id: Optional[str] = Query(None),
    remark_id: Optional[int] = Query(None),
    loc_id: Optional[str] = Query(None),
    remark_category_id: Optional[int] = Query(None)
):
    data = fetch_remark_data(
        user_id=user_id,
        item_id=item_id,
        remark_id=remark_id,
        loc_id=loc_id,
        remark_category_id=remark_category_id
    )
    return {"count": len(data), "data": data}
