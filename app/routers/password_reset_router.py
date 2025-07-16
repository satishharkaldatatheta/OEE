from fastapi import APIRouter, HTTPException, Query
from app.models.password_reset_model import PasswordResetRequest
from app.models.password_update_model import PasswordUpdateRequest
from app.services.password_reset_service import (
    create_password_reset_token,
    verify_token_validity,
    update_password_with_token
)

router = APIRouter()

@router.post("/request-password-reset")
async def request_password_reset(request: PasswordResetRequest):
    success = create_password_reset_token(request.email)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Password reset link sent to your email."}


@router.get("/reset-password-token-verify")
async def verify_reset_token(token: str = Query(...)):
    from app.services.password_reset_service import verify_token_validity

    is_valid = verify_token_validity(token)
    return is_valid 


@router.post("/reset-password")
async def reset_password(data: PasswordUpdateRequest):
    success = update_password_with_token(data.token, data.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password updated successfully"}
