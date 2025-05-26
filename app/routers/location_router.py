from fastapi import APIRouter
from app.services.location_service import (
    get_all_locations,
    get_location_by_id,
    get_locations_by_country
)

router = APIRouter()

@router.get("/locations")
async def get_all():
    locations = get_all_locations()
    return [
        {"id": loc[0], "name": loc[1], "address": loc[2], "country": loc[3]}
        for loc in locations
    ]

@router.get("/locations/{loc_id}")
async def get_by_id(loc_id: str):
    location = get_location_by_id(loc_id)
    if location:
        return {"id": location[0], "name": location[1], "address": location[2], "country": location[3]}
    else:
        return {"error": "Location not found"}

@router.get("/locations/country/{country}")
async def get_by_country(country: str):
    locations = get_locations_by_country(country)
    if locations:
        return [
            {"id": loc[0], "name": loc[1], "address": loc[2], "country": loc[3]}
            for loc in locations
        ]
    else:
        return {"error": "No locations found for this country"}
