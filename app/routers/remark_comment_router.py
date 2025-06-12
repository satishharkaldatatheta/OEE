# remark_comment_router.py

from fastapi import APIRouter, Query
from typing import Optional, List
from app.services.remark_comment_service import fetch_grouped_remark_comments

router = APIRouter()

@router.get("/remark_comment")
def get_grouped_remark_comments(
    remark_category_id: Optional[int] = Query(None),
    remark_id: Optional[int] = Query(None)
):
    data = fetch_grouped_remark_comments(remark_category_id, remark_id)
    return {"data": data}