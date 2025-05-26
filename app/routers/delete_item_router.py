from fastapi import APIRouter, Form, HTTPException
from app.services.delete_item_service import delete_item

router = APIRouter()

@router.delete("/item/delete")
def delete_item_api(
    item_id: str = Form(..., description="Item ID to delete")
):
    result = delete_item(item_id=item_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
