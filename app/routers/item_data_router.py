from fastapi import APIRouter
from app.services.item_data_service import get_item_data

router = APIRouter()

@router.get("/item_data/{item_id}")
def get_item_data_by_id(item_id: str):
    data = get_item_data(item_id)
    return {"item_id": item_id, "data": data}
