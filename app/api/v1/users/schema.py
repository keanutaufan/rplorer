from pydantic import BaseModel
from datetime import datetime

class RegisterSchema(BaseModel):
    username: str
    password: str 
    display_name: str
    bio: str | None = None


class LoginSchema(BaseModel):
    username: str
    password: str


class UserResponseSchema(BaseModel):
    username: str
    display_name: str
    bio: str | None
    created_at: datetime
    updated_at: datetime