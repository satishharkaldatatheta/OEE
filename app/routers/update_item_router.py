from fastapi import APIRouter, Form, HTTPException
from typing import Optional
from app.services.update_item_service import update_item

router = APIRouter()

@router.put("/item/update")
def update_item_api(
    item_id: str = Form(..., description="Item ID to update"),
    name: Optional[str] = Form(None, description="New name of the item"),
    loc_id: Optional[str] = Form(None, description="New location ID of the item"),
):
    result = update_item(item_id=item_id, name=name, loc_id=loc_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
