from fastapi import APIRouter
from typing import List
from app.services import bookmark_service

router = APIRouter()

@router.post("/bookmarks/")
def add_bookmark(user_id: int, equipment_id: str):
    return bookmark_service.add_bookmark(user_id, equipment_id)

@router.delete("/bookmarks/")
def remove_bookmark(user_id: int, equipment_id: str):
    return bookmark_service.remove_bookmark(user_id, equipment_id)

@router.get("/bookmarks/check")
def check_bookmark(user_id: int, equipment_id: str):
    return bookmark_service.is_bookmarked(user_id, equipment_id)

@router.get("/bookmarks/{user_id}", response_model=List[str])
def get_user_bookmarks(user_id: int):
    return bookmark_service.get_user_bookmarks(user_id)