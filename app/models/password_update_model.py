# app/models/password_update_model.py
from pydantic import BaseModel, Field

class PasswordUpdateRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)
