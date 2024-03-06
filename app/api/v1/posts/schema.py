from pydantic import BaseModel

class CreatePostSchema(BaseModel):
    content: str