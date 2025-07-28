from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.language_service import get_languages

router = APIRouter()

class LanguageOut(BaseModel):
    language_id: int
    language_name: str
    iso_code: str

@router.get("/languages")
def read_languages():
    """
    Retrieve the list of all supported languages.
    """
    return get_languages()