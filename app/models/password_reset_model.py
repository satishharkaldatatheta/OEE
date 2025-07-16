# app/models/password_reset_model.py
from pydantic import BaseModel, EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr
