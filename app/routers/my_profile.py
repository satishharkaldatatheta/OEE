from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from typing import Optional
import shutil
from pathlib import Path
from app.services.my_profile_service import update_user_profile

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
    profile_picture: Optional[UploadFile] = File(None)
):
    profile_picture_url = None

    if profile_picture:
        # Validate image type
        if profile_picture.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPEG and PNG files are allowed")

        try:
            # Determine upload directory
            BASE_DIR = Path(__file__).resolve().parents[2]
            UPLOAD_DIR = BASE_DIR / "ProfileImage"
            UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

            # Save file
            file_ext = Path(profile_picture.filename).suffix.lower()
            file_name = f"user_{user_id}{file_ext}"
            file_path = UPLOAD_DIR / file_name

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_picture.file, buffer)

            print(f"✅ Saved profile picture to: {file_path}")
            profile_picture_url = f"/api/ProfileImage/{file_name}"

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
            profile_picture_url=profile_picture_url,
            country_id=country_id,
            language_id=language_id,
            timezone_id=timezone_id
        )
        return {"message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
