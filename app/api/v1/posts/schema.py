from pydantic import BaseModel

class CreatePostSchema(BaseModel):
    content: str
    media: list[str]


class UpdatePostSchema(BaseModel):
    content: str


class UpdatePostMediaSchema(BaseModel):
    media_id: str