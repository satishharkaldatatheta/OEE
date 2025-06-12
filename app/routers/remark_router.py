from fastapi import APIRouter, Form, HTTPException
from app.services.remark_service import insert_remark

router = APIRouter()

@router.post("/remark")
def create_remark(
    user_id: int = Form(...),
    remark_id: int = Form(...),
    remark_category_id: int = Form(...),
    item_id: str = Form(...),  
    loc_id: str = Form(...),  
    status: str = Form(...),
    oee: float = Form(...),
    problem: str = Form(...)
):
    try:
        inserted_id = insert_remark(
            user_id=user_id,
            remark_id=remark_id,
            remark_category_id=remark_category_id,
            item_id=item_id,
            loc_id=loc_id,
            status=status,
            oee=oee,
            problem=problem
        )
        return {"message": "Remark inserted successfully", "remark_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))