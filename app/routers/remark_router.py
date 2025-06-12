from typing import List
from fastapi import APIRouter, Form, HTTPException
from app.services.remark_service import insert_multiple_remarks

router = APIRouter()

@router.post("/remark")
def create_remark(
    user_id: int = Form(...),
    remark_ids: List[int] = Form(...),
    remark_category_ids: List[int] = Form(...),
    item_id: str = Form(...),  
    loc_id: str = Form(...),  
    status: str = Form(...),
    oee: float = Form(...)
):
    try:
        if len(remark_ids) != len(remark_category_ids):
            raise HTTPException(status_code=400, detail="Each remark must have a corresponding category.")

        inserted_ids = insert_multiple_remarks(
            user_id=user_id,
            remark_ids=remark_ids,
            remark_category_ids=remark_category_ids,
            item_id=item_id,
            loc_id=loc_id,
            status=status,
            oee=oee
        )
        return {
            "message": "Remarks inserted successfully",
            "inserted_remark_ids": inserted_ids
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
