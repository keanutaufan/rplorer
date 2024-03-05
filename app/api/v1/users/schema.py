from pydantic import BaseModel

class RegisterSchema(BaseModel):
    username: str
    password: str 
    display_name: str
    bio: str | None = None


class LoginSchema(BaseModel):
    username: str
    password: str