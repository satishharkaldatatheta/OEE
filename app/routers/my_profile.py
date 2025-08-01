from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from typing import Optional
import shutil
from pathlib import Path
from datetime import datetime
import os
from app.services.my_profile_service import update_user_profile, get_current_profile_picture_url

router = APIRouter()

@router.post("/my_profile")
async def my_profile(
    user_id: int = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    address: Optional[str] = Form(None),
    phone_number: Optional[str] = Form(None),
    postal_code: Optional[str] = Form(None),
    country_id: Optional[int] = Form(None),
    language_id: Optional[int] = Form(None),
    timezone_id: Optional[int] = Form(None),
    profile_picture_url: Optional[UploadFile] = File(None)
):
    profile_picture_path = None

    if profile_picture_url:
        if profile_picture_url.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPEG and PNG files are allowed")

        try:
            BASE_DIR = Path(__file__).resolve().parents[2]
            UPLOAD_DIR = BASE_DIR / "ProfileImage"
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

            # Add timestamp to filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_ext = Path(profile_picture_url.filename).suffix.lower()
            file_name = f"user_{user_id}_{timestamp}{file_ext}"
            file_path = UPLOAD_DIR / file_name

            # Delete old picture if it exists
            old_picture_url = get_current_profile_picture_url(user_id)
            if old_picture_url:
                old_file_path = BASE_DIR / old_picture_url.strip("/")
                if old_file_path.exists():
                    os.remove(old_file_path)

            # Save new picture
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_picture_url.file, buffer)

            print(f"Saved profile picture to: {file_path}")
            profile_picture_path = f"/api/ProfileImage/{file_name}"

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save image: {e}")

    try:
        update_user_profile(
            user_id=user_id,
            firstname=firstname,
            lastname=lastname,
            address=address,
            phone_number=phone_number,
            postal_code=postal_code,
            profile_picture_url=profile_picture_path,
            country_id=country_id,
            language_id=language_id,
            timezone_id=timezone_id
        )
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
