from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.country_service import get_countries

router = APIRouter()

class CountryOut(BaseModel):
    country_id: int
    country_name: str

@router.get("/countries")
def read_countries():
    """
    Retrieve the list of all countries.
    """
    return get_countries()